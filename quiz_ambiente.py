import streamlit as st
import time
import random

# ---------------------------------------------
# Quiz Ambiental Interativo — Versão Aprimorada com Música e Confete
# ---------------------------------------------

st.set_page_config(page_title="Quiz Ambiental — Guardiões da Terra 🌎",
                   page_icon="🌿",
                   layout="wide",
                   initial_sidebar_state="expanded")

# -------------------- CSS + JS --------------------
st.markdown("""
<style>
:root{
    --bg-start: #e6fff0;
    --bg-end: #d0f4ea;
    --card: rgba(255,255,255,0.95);
    --accent: #2e8b57;
}
html, body {
    background: linear-gradient(180deg, var(--bg-start), var(--bg-end));
}
.main-card{
    background: var(--card);
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(10,80,20,0.08);
    margin-bottom: 18px;
}
h1, h2 { color: var(--accent); text-align:center; }
.question-card{ border-left:6px solid var(--accent); padding:16px; border-radius:10px; margin-bottom:12px;}
.small-muted{ color: #2f6b3f; opacity:0.85; font-size:14px }
.stButton>button{ border-radius:12px; padding:10px 18px; font-size:16px }
.progress-green{ height:18px; background: linear-gradient(90deg,#4cd964,#2e8b57); border-radius:10px }
.badge{ background: linear-gradient(90deg,#ffd36b,#ff9a3c); padding:8px 12px; border-radius:12px; font-weight:600 }
.planet-wrap{ display:flex; justify-content:center; margin-bottom:12px }
.planet{ width:120px; height:120px; border-radius:50%; background: radial-gradient(circle at 35% 35%, #79c68b, #2e8b57); box-shadow:0 6px 20px rgba(0,0,0,0.08); transform-origin:center; animation: spinPlanet 18s linear infinite;}
@keyframes spinPlanet{ from{ transform: rotate(0deg) } to{ transform: rotate(360deg) } }
.confetti-canvas{ position:fixed; left:0; top:0; width:100%; height:100%; pointer-events:none; z-index:9999 }
.fade-in{ animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn{ from{ opacity:0; transform: translateY(8px) } to{ opacity:1; transform: translateY(0) } }
@media (max-width: 700px){ .planet{ width:90px; height:90px } }
</style>

<script>
window.playGood = function(){
    try{
        const ctx = new (window.AudioContext||window.webkitAudioContext)();
        const o = ctx.createOscillator();
        const g = ctx.createGain();
        o.type = 'sine'; o.frequency.value = 880;
        g.gain.value = 0.05;
        o.connect(g); g.connect(ctx.destination);
        o.start(); o.stop(ctx.currentTime + 0.12);
    }catch(e){}
};
window.playBad = function(){
    try{
        const ctx = new (window.AudioContext||window.webkitAudioContext)();
        const o = ctx.createOscillator();
        const g = ctx.createGain();
        o.type = 'square'; o.frequency.value = 220;
        g.gain.value = 0.06;
        o.connect(g); g.connect(ctx.destination);
        o.start(); o.stop(ctx.currentTime + 0.22);
    }catch(e){}
};
// Confetti
window.launchConfetti = function(){
    const colors = ['#ff6b6b','#ffd93d','#6bf178','#6bbcff','#b86bff'];
    for(let i=0;i<60;i++){
        const el = document.createElement('div');
        el.style.position='fixed'; el.style.left=(Math.random()*100)+'%'; el.style.top='-5%';
        el.style.width='8px'; el.style.height='12px';
        el.style.background=colors[Math.floor(Math.random()*colors.length)];
        el.style.opacity='0.95';
        el.style.transform='rotate('+Math.random()*360+'deg)';
        el.style.zIndex=9999; el.style.borderRadius='2px';
        el.style.transition='transform 3s linear, top 3s linear, left 3s linear, opacity 3s linear';
        document.body.appendChild(el);
        setTimeout(()=>{ el.style.top=(80+Math.random()*20)+'%';
        el.style.left=(Math.random()*100)+'%';
        el.style.transform='translateY(0) rotate('+Math.random()*720+'deg)';
        el.style.opacity='0'; },20);
        setTimeout(()=>el.remove(),3500);
    }
};
</script>
""", unsafe_allow_html=True)

# -------------------- PERGUNTAS --------------------
QUESTOES = [
    {"q":"Evito jogar lixo em locais inadequados.", "hint":"Pequenas atitudes urbanas reduzem muito a poluição local."},
    {"q":"Separo materiais recicláveis em casa.", "hint":"Separar facilita a reciclagem e reduz a extração de recursos."},
    {"q":"Procuro reduzir o uso de plástico descartável.", "hint":"Plásticos descartáveis levam décadas para se decompor."},
    {"q":"Economizo água nas tarefas do dia a dia.", "hint":"Reduzir o tempo no banho e consertar vazamentos ajuda muito."},
    {"q":"Desligo luzes e aparelhos que não estão sendo usados.", "hint":"Poupar energia reduz demanda e emissões."},
]

FUN_FACTS = [
    "Reciclar uma lata de alumínio economiza energia suficiente para ouvir rádio por 3 horas.",
    "Plantar árvores ajuda a combater o aquecimento global.",
    "Reduzir o desperdício de comida economiza água, energia e transporte.",
]

def calcular_categoria(total, max_pontos):
    proporcao = total / max_pontos
    if proporcao >= 0.85:
        return "Campeão Ambiental", "🏆"
    elif proporcao >= 0.6:
        return "Protetor Verde", "🌿"
    elif proporcao >= 0.4:
        return "Aprendiz Consciente", "🌱"
    else:
        return "Iniciante — Hora de Agir", "🌍"

def carregar_ranking():
    if 'ranking' not in st.session_state:
        st.session_state['ranking'] = []
    return st.session_state['ranking']

def salvar_no_ranking(nome, pontos):
    r = carregar_ranking()
    r.append({"nome":nome, "pontos":pontos, "ts": time.time()})
    r.sort(key=lambda x: x['pontos'], reverse=True)
    st.session_state['ranking'] = r[:20]

# -------------------- QUIZ --------------------
def iniciar_quiz():
    perguntas_idx = list(range(len(QUESTOES)))
    random.shuffle(perguntas_idx)
    st.session_state['perguntas_idx'] = perguntas_idx
    st.session_state['respostas'] = []
    st.session_state['cur_idx'] = 0
    st.session_state['iniciado'] = True
    st.session_state['finished'] = False
    st.session_state['start_time'] = time.time()

# Sidebar
st.sidebar.markdown("# ⚙️ Configurações")
with st.sidebar.form(key='config'):
    nome = st.text_input("Seu nome (opcional)")
    mostrar_sons = st.checkbox("Habilitar sons curtos", value=True)
    started = st.form_submit_button("Aplicar")

# Tela inicial
if not st.session_state.get('iniciado'):
    st.markdown('<div class="main-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="planet-wrap"><div class="planet"></div></div>', unsafe_allow_html=True)
    st.title("Quiz Ambiental — Guardiões da Terra 🌎")
    st.write("Descubra o quanto você ajuda o planeta com atitudes simples!")
    if st.button("🌱 Iniciar Quiz"):
        iniciar_quiz()
        st.markdown("""
        <audio autoplay loop>
            <source src="https://cdn.pixabay.com/download/audio/2021/09/27/audio_13ec4d7a28.mp3" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Perguntas
if st.session_state.get('iniciado') and not st.session_state.get('finished'):
    idx = st.session_state['cur_idx']
    perguntas_idx = st.session_state['perguntas_idx']
    if idx < len(perguntas_idx):
        qidx = perguntas_idx[idx]
        pergunta = QUESTOES[qidx]

        st.markdown('<div class="main-card fade-in">', unsafe_allow_html=True)
        st.markdown(f"### Pergunta {idx+1} de {len(QUESTOES)}")
        st.markdown(f"<div class='question-card'><b>{pergunta['q']}</b></div>", unsafe_allow_html=True)
        resposta = st.slider("Escolha sua resposta:", 1, 3, 2, key=f'q_{idx}')

        if st.button("✅ Salvar resposta"):
            st.session_state['respostas'].append(resposta)
            if mostrar_sons:
                if resposta == 3:
                    st.markdown("<script>window.playGood();window.launchConfetti();</script>", unsafe_allow_html=True)
                else:
                    st.markdown("<script>window.playBad()</script>", unsafe_allow_html=True)
            st.session_state['cur_idx'] += 1
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.session_state["finished"] = True
        st.experimental_rerun()

# Resultado final
if st.session_state.get('finished'):
    respostas = st.session_state.get('respostas', [])
    if not respostas or len(respostas) == 0:
        st.warning("Responda pelo menos uma pergunta antes de finalizar 🌱")
        st.stop()

    total = sum(respostas)
    max_p = len(QUESTOES) * 3
    categoria, emoji = calcular_categoria(total, max_p)

    st.markdown('<div class="main-card fade-in">', unsafe_allow_html=True)
    st.header("📊 Resultado Final")
    st.markdown(f"<h3 style='text-align:center'>{emoji} {categoria}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;font-size:18px'>Pontuação: <b>{total}</b> de {max_p}</p>", unsafe_allow_html=True)
    st.markdown("<script>window.launchConfetti();window.playGood();</script>", unsafe_allow_html=True)

    if st.button("🔁 Reiniciar Quiz"):
        st.session_state.clear()
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
