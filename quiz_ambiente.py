import streamlit as st
import time
import random
import math
import json

# ---------------------------------------------
# Quiz Ambiental Interativo — Versão Aprimorada
# Arquivo: quiz_ambiente.py
# Execute com: streamlit run quiz_ambiente.py
# Objetivo: transformar o quiz original em uma experiência mais imersiva,
# com transições, feedback animado, gamificação, dicas educativas e confetes.
# Tudo roda dentro do Streamlit sem dependências extras além do próprio Streamlit.
# ---------------------------------------------

# -------------------- CONFIGURAÇÕES --------------------
st.set_page_config(page_title="Quiz Ambiental — Guardiões da Terra 🌎",
                   page_icon="🌿",
                   layout="wide",
                   initial_sidebar_state="expanded")

# -------------------- ESTILO GLOBAL (CSS + JS) --------------------
# Comentários: usamos CSS e pequenos trechos de JS (injetados via st.markdown)
# para efeitos visuais e para controlar animações/sons via WebAudio API.

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
/* Container principal */
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
/* planet animation */
.planet-wrap{ display:flex; justify-content:center; margin-bottom:12px }
.planet{ width:120px; height:120px; border-radius:50%; background: radial-gradient(circle at 35% 35%, #79c68b, #2e8b57); box-shadow:0 6px 20px rgba(0,0,0,0.08); transform-origin:center; animation: spinPlanet 18s linear infinite;}
@keyframes spinPlanet{ from{ transform: rotate(0deg) } to{ transform: rotate(360deg) } }
/* confetti placeholder - JS will create real confetti */
.confetti-canvas{ position:fixed; left:0; top:0; width:100%; height:100%; pointer-events:none; z-index:9999 }
/* entrance animation */
.fade-in{ animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn{ from{ opacity:0; transform: translateY(8px) } to{ opacity:1; transform: translateY(0) } }

@media (max-width: 700px){ .planet{ width:90px; height:90px } }
</style>

<script>
// Funções de som via WebAudio (gera sons curtos sem precisar de arquivos)
window.playGood = function(){ try{ const ctx = new (window.AudioContext||window.webkitAudioContext)(); const o = ctx.createOscillator(); const g = ctx.createGain(); o.type = 'sine'; o.frequency.value = 880; g.gain.value = 0.05; o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.12); }catch(e){} };
window.playBad = function(){ try{ const ctx = new (window.AudioContext||window.webkitAudioContext)(); const o = ctx.createOscillator(); const g = ctx.createGain(); o.type = 'square'; o.frequency.value = 220; g.gain.value = 0.06; o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.22); }catch(e){} };

// Confetti (basic) - cria pequenos elementos coloridos e anima
window.launchConfetti = function(){ const colors = ['#ff6b6b','#ffd93d','#6bf178','#6bbcff','#b86bff']; for(let i=0;i<60;i++){ const el = document.createElement('div'); el.style.position='fixed'; el.style.left=(Math.random()*100)+'%'; el.style.top='-5%'; el.style.width='8px'; el.style.height='12px'; el.style.background=colors[Math.floor(Math.random()*colors.length)]; el.style.opacity='0.95'; el.style.transform='rotate('+Math.random()*360+'deg)'; el.style.zIndex=9999; el.style.borderRadius='2px'; el.style.transition='transform 3s linear, top 3s linear, left 3s linear, opacity 3s linear'; document.body.appendChild(el); setTimeout(()=>{ el.style.top=(80+Math.random()*20)+'%'; el.style.left=(Math.random()*100)+'%'; el.style.transform='translateY(0) rotate('+Math.random()*720+'deg)'; el.style.opacity='0'; },20); setTimeout(()=>el.remove(),3500); } };
</script>
""", unsafe_allow_html=True)

# -------------------- DADOS DO QUIZ --------------------
QUESTOES = [
    {"q":"Evito jogar lixo em locais inadequados.", "hint":"Pequenas atitudes urbanas reduzem muito a poluição local."},
    {"q":"Separo materiais recicláveis em casa.", "hint":"Separar facilita a reciclagem e reduz a extração de recursos."},
    {"q":"Procuro reduzir o uso de plástico descartável.", "hint":"Plásticos descartáveis levam décadas para se decompor."},
    {"q":"Economizo água nas tarefas do dia a dia.", "hint":"Reduzir o tempo no banho e consertar vazamentos ajuda muito."},
    {"q":"Desligo luzes e aparelhos que não estão sendo usados.", "hint":"Poupar energia reduz demanda e emissões."},
    {"q":"Participo ou apoio ações de preservação ambiental.", "hint":"A ação coletiva gera mudanças maiores."},
    {"q":"Levo em conta o impacto ambiental ao comprar produtos.", "hint":"Escolher produtos com menos embalagem ajuda."},
    {"q":"Acredito que atitudes individuais ajudam o planeta.", "hint":"Somadas, pequenas atitudes geram grande impacto."},
    {"q":"Procuro aprender mais sobre meio ambiente e biodiversidade.", "hint":"Conhecimento transforma comportamento."},
    {"q":"Acho importante cobrar políticas públicas ambientais.", "hint":"Engajar-se politicamente fortalece a proteção ambiental."},
    {"q":"Uso transporte público ou bicicleta para reduzir emissões.", "hint":"Reduzir carros na rua melhora a qualidade do ar."},
    {"q":"Planto árvores ou cuido de plantas em casa.", "hint":"Plantas ajudam regulação térmica e qualidade do ar."},
    {"q":"Evito o desperdício de alimentos no meu dia a dia.", "hint":"Desperdício impacta recursos e aumenta emissões."}
]

FUN_FACTS = [
    "Reciclar uma lata de alumínio economiza energia suficiente para ouvir rádio por 3 horas.",
    "Plantar árvores ajuda a combater o aquecimento global — cada árvore absorve CO2 ao longo dos anos!",
    "Reduzir o desperdício de comida economiza água, energia e transporte — menos emissões no final." ,
    "Restaurar áreas degradadas pode recuperar biodiversidade e serviços ecossistêmicos locais.",
    "A pegada de carbono de alimentos processados costuma ser maior que a de alimentos frescos locais."    
]

# -------------------- FUNÇÕES AUXILIARES --------------------

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

# -------------------- LÓGICA DO QUIZ --------------------

def iniciar_quiz(dificuldade='Medio'):
    perguntas_idx = list(range(len(QUESTOES)))
    random.shuffle(perguntas_idx)
    st.session_state['perguntas_idx'] = perguntas_idx
    st.session_state['respostas'] = []
    st.session_state['cur_idx'] = 0
    st.session_state['iniciado'] = True
    st.session_state['start_time'] = time.time()
    st.session_state['dificuldade'] = dificuldade

# -------------------- UI: TELA INICIAL --------------------

st.sidebar.markdown("# ⚙️ Configurações")
with st.sidebar.form(key='config'):
    nome = st.text_input("Seu nome (opcional)")
    dificuldade = st.selectbox("Nível de dificuldade", options=['Facil','Medio','Dificil'], index=1)
    mostrar_sons = st.checkbox("Habilitar sons curtos (WebAudio)", value=True)
    show_tips = st.checkbox("Mostrar dicas educativas após cada pergunta", value=True)
    started = st.form_submit_button("Aplicar")

col1, col2 = st.columns([2,1])
with col1:
    st.markdown('<div class="main-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="planet-wrap"><div class="planet" title="Planeta Guardião"></div></div>', unsafe_allow_html=True)
    st.title("Quiz Ambiental — Guardiões da Terra 🌎")
    st.markdown("""
    <p class='small-muted'>Teste seus hábitos e descubra o quão preparado você está para proteger o meio ambiente.
    Um quiz educativo, bonito e com feedbacks imediatos.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🏅 Ranking Rápido")
    ranking = carregar_ranking()
    if ranking:
        for i, item in enumerate(ranking[:5], start=1):
            st.write(f"{i}. {item['nome'] or 'Anônimo'} — {item['pontos']} pts")
    else:
        st.write("Seja o primeiro a marcar pontos!")
    st.markdown('</div>', unsafe_allow_html=True)

if 'iniciado' not in st.session_state or not st.session_state.get('iniciado'):
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        if st.button("Iniciar quiz 🌱"):
            iniciar_quiz(dificuldade)
            st.experimental_rerun()
    with col_b:
        if st.button("Ver instruções ⓘ"):
            st.info("Responda cada pergunta de 1 (discordo totalmente) a 5 (concordo totalmente). Use o botão 'Próxima' para avançar. Dicas aparecerão quando ativadas.")
    with col_c:
        if st.button("Exibir perguntas (todas)"):
            st.subheader('Modo rápido: todas as perguntas')
            respostas = []
            for i, quest in enumerate(QUESTOES, start=1):
                st.markdown(f"**{i}. {quest['q']}**")
                val = st.slider("",1,5,3,key=f'fast_{i}')
                respostas.append(val)
            if st.button('Ver Resultado (modo rápido)'):
                exibir_resultado(respostas, nome)

if st.session_state.get('iniciado'):
    idx = st.session_state['cur_idx']
    perguntas_idx = st.session_state['perguntas_idx']
    
    if idx < len(perguntas_idx):  # Verifica se o índice é válido
        qidx = perguntas_idx[idx]
        pergunta = QUESTOES[qidx]
        max_p = len(QUESTOES) * 5

        container = st.empty()
        with container.container():
            st.markdown('<div class="main-card fade-in">', unsafe_allow_html=True)
            progresso_pct = int(((idx) / len(QUESTOES)) * 100)
            st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center'><div><h2>Pergunta {idx+1} de {len(QUESTOES)}</h2><div class='small-muted'>Nível: <span class='badge'>{st.session_state['dificuldade']}</span></div></div><div style='width:45%'><div style='background:#e6f7ee;border-radius:10px;padding:4px'><div class='progress-green' style='width:{progresso_pct}%'></div></div></div></div>", unsafe_allow_html=True)

            st.markdown(f"<div class='question-card'><b>{pergunta['q']}</b></div>", unsafe_allow_html=True)

            col1, col2 = st.columns([3,1])
            with col1:
                resposta = st.slider("Escolha sua resposta:", 1, 5, 3, key=f'q_{idx}', help='1 = Discordo totalmente ... 5 = Concordo totalmente')
                if show_tips:
                    st.markdown(f"<div class='small-muted'>Dica: {pergunta['hint']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='small-muted'>Fun Fact: {random.choice(FUN_FACTS)}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown('<div style="display:flex;flex-direction:column;gap:8px">', unsafe_allow_html=True)
                if st.button('✅ Salvar resposta'):
                    st.session_state['respostas'].append(resposta)
                    if mostrar_sons:
                        if resposta >= 4:
                            st.markdown("<script>window.playGood()</script>", unsafe_allow_html=True)
                        else:
                            st.markdown("<script>window.playBad()</script>", unsafe_allow_html=True)
                    st.session_state['cur_idx'] += 1
                    if st.session_state['cur_idx'] >= len(QUESTOES):
                        st.session_state['finished'] = True
                    st.experimental_rerun()
                if st.button('💡 Dica extra'):
                    st.warning('Pense em ações locais: falar com vizinhos, reduzir embalagens e consertar vazamentos.')
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.session_state['finished'] = True
        st.experimental_rerun()

if st.session_state.get('finished'):
    respostas = st.session_state.get('respostas', [])
    if len(respostas) > 0:  # Verifica se há respostas antes de prosseguir
        total = sum(respostas)
        max_p = len(QUESTOES) * 5
        categoria, emoji = calcular_categoria(total, max_p)
        
        st.markdown('<div class="main-card fade-in">', unsafe_allow_html=True)
        st.header('📊 Resultado Final')
        st.markdown(f"<h3 style='text-align:center'>{emoji} {categoria}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:18px'>Pontuação: <b>{total}</b> de {max_p}</p>", unsafe_allow_html=True)
        
        st.write('Calculando insights...')
        for i in range(20):
            time.sleep(0.02)
        st.success('Pronto! Veja abaixo suas recomendações personalizadas 🌱')
        
        media = total / len(QUESTOES)
        dicas = []
        if media < 3:
            dicas.append('Foque em reduzir desperdício e economizar água: pequenos hábitos diários geram grande impacto.')
        else:
            dicas.append('Ótimo! Ajude outras pessoas compartilhando o que sabe e engajando em ações comunitárias.')
        dicas.append('Participe de campanhas locais e proponha ideias à sua escola ou comunidade.')
        dicas.append('Considere plantar árvores ou apoiar projetos de restauração em sua região.')
        
        st.markdown('<ul>', unsafe_allow_html=True)
        for d in dicas:
            st.markdown(f"<li class='small-muted'>{d}</li>", unsafe_allow_html=True)
        st.markdown('</ul>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button('🎉'

