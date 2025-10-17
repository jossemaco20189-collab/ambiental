# app.py
# Quiz Ambiental — Guardiões da Terra (Versão Escura e Responsiva)
# Autor: aprimorado por ChatGPT a pedido do usuário
# Rode: streamlit run app.py

import streamlit as st
import time
import random
from datetime import datetime

# ---------------------------
# CONFIGURAÇÃO INICIAL
# ---------------------------
st.set_page_config(
    page_title="Quiz Ambiental — Guardiões da Terra",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# DADOS DAS QUESTÕES
# ---------------------------
QUESTOES = [
    {"q": "Evito jogar lixo em locais inadequados.",
     "hint": "Descartar corretamente evita entupimentos, poluição dos rios e prejuízo à fauna.",
     "fact": "O lixo que vai para rios costuma terminar no oceano — evitar descarte impróprio protege ecossistemas costeiros."},
    {"q": "Separo materiais recicláveis em casa.",
     "hint": "Separar facilita a reciclagem e reduz a extração de recursos naturais.",
     "fact": "Reciclar papel evita derrubada de árvores — uma tonelada de papel reciclado salva cerca de 17 árvores."},
    {"q": "Procuro reduzir o uso de plástico descartável.",
     "hint": "Plásticos descartáveis levam séculos para se decompor e afetam a vida marinha.",
     "fact": "As microfibras plásticas já foram encontradas até em águas potáveis e peixes consumidos por humanos."},
    {"q": "Economizo água nas tarefas do dia a dia.",
     "hint": "Reduzir o tempo de banho e consertar vazamentos economiza milhares de litros por ano.",
     "fact": "Um vazamento pequeno pode desperdiçar mais de 200 litros por dia — conserte sempre que notar."},
    {"q": "Desligo luzes e aparelhos que não estão sendo usados.",
     "hint": "Desligar economiza energia e reduz emissões associadas à geração elétrica.",
     "fact": "Equipamentos em standby ainda consomem eletricidade — desligue da tomada."},
    {"q": "Participo ou apoio ações de preservação ambiental.",
     "hint": "A ação coletiva gera mudanças significativas em políticas e comportamento.",
     "fact": "Mutirões locais podem restaurar habitats e aumentar a biodiversidade."},
    {"q": "Levo em conta o impacto ambiental ao comprar produtos.",
     "hint": "Escolher produtos duráveis e com menos embalagem reduz resíduos.",
     "fact": "Produtos sustentáveis normalmente utilizam menos recursos de produção."},
    {"q": "Acredito que atitudes individuais ajudam o planeta.",
     "hint": "Atitudes somadas transformam mercados e políticas públicas.",
     "fact": "Campanhas de consumo consciente já mudaram práticas de grandes empresas."},
    {"q": "Procuro aprender mais sobre meio ambiente e biodiversidade.",
     "hint": "Conhecimento inspira ação e escolhas melhores no dia a dia.",
     "fact": "Comunidades educadas alcançam melhores resultados em conservação."},
    {"q": "Acho importante cobrar políticas públicas ambientais.",
     "hint": "Cobrança e participação influenciam legislações e fiscalizações.",
     "fact": "A pressão popular foi decisiva para criação de áreas protegidas no mundo."},
    {"q": "Uso transporte público ou bicicleta para reduzir emissões.",
     "hint": "Menos carros = menos emissões e menos congestionamento.",
     "fact": "Trocar trajetos curtos de carro por bicicleta reduz sua pegada de carbono anual."},
    {"q": "Planto árvores ou cuido de plantas em casa.",
     "hint": "Plantas ajudam a regular temperatura e limpar o ar localmente.",
     "fact": "Árvores maduras capturam toneladas de CO₂ e melhoram ecossistemas urbanos."},
    {"q": "Evito o desperdício de alimentos no meu dia a dia.",
     "hint": "Planejar refeições e armazenar corretamente reduz desperdício e emissões.",
     "fact": "Um terço dos alimentos produzidos no mundo é desperdiçado — evite isso!"}
]

# ---------------------------
# ESTILO GLOBAL (CSS + JS)
# ---------------------------
st.markdown("""
<style>
:root {
  --bg-dark: #0f1c13;
  --card-dark: #18281d;
  --accent: #48c774;
  --accent-dark: #3aa564;
  --gold: #ffd36b;
  --text-light: #f2f2f2;
  --muted: #a3bfa8;
}
html, body {
  background: var(--bg-dark);
  color: var(--text-light);
}
.main-card {
  background: var(--card-dark);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.4);
  margin-bottom: 18px;
}
h1, h2, h3 { color: var(--accent); }
.question-card {
  border-left: 5px solid var(--accent);
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 10px;
  color: var(--text-light);
}
.small-muted { color: var(--muted); font-size: 14px; }
.badge {
  background: linear-gradient(90deg, var(--gold), #ff9a3c);
  color: #222;
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 600;
}
.stButton>button {
  background: linear-gradient(90deg, var(--accent), var(--accent-dark));
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 600;
  width: 100%;
}
.stButton>button:hover {
  background: var(--accent-dark);
}
.progress-track {
  background: rgba(255,255,255,0.1);
  border-radius: 10px;
}
.progress-fill {
  height: 10px;
  background: linear-gradient(90deg, var(--accent), var(--gold));
  border-radius: 8px;
  transition: width 700ms ease;
}
@media (max-width: 900px) {
  .main-card { padding: 14px !important; }
  .question-card { padding: 10px !important; font-size: 15px; }
  h1 { font-size: 20px !important; text-align:center; }
  h2 { font-size: 18px !important; text-align:center; }
  .stSlider>div { width: 100% !important; }
  .stButton>button { width: 100% !important; }
}
</style>

<script>
window.playGood = function(){try{const c=new (window.AudioContext||window.webkitAudioContext)();const o=c.createOscillator();const g=c.createGain();o.type='sine';o.frequency.value=880;g.gain.value=0.04;o.connect(g);g.connect(c.destination);o.start();o.stop(c.currentTime+0.12);}catch(e){}};
window.playBad = function(){try{const c=new (window.AudioContext||window.webkitAudioContext)();const o=c.createOscillator();const g=c.createGain();o.type='triangle';o.frequency.value=220;g.gain.value=0.06;o.connect(g);g.connect(c.destination);o.start();o.stop(c.currentTime+0.22);}catch(e){}};
window.launchConfetti = function(){const colors=['#48c774','#ffd36b','#3aa564','#6bbcff','#b86bff'];for(let i=0;i<70;i++){const el=document.createElement('div');el.style.position='fixed';el.style.left=(Math.random()*100)+'%';el.style.top='-5%';el.style.width=(6+Math.random()*6)+'px';el.style.height=(10+Math.random()*10)+'px';el.style.background=colors[Math.floor(Math.random()*colors.length)];el.style.opacity='0.9';el.style.transform='rotate('+Math.random()*360+'deg)';el.style.zIndex=9999;el.style.borderRadius='2px';el.style.transition='transform 3s linear, top 3s linear, opacity 3s linear';document.body.appendChild(el);setTimeout(()=>{el.style.top=(80+Math.random()*20)+'%';el.style.transform='rotate('+Math.random()*720+'deg)';el.style.opacity='0';},20);setTimeout(()=>el.remove(),3500);}};
</script>
""", unsafe_allow_html=True)

# ---------------------------
# ESTADO
# ---------------------------
def init_state():
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
        st.session_state['iniciado'] = False
        st.session_state['finished'] = False
        st.session_state['perguntas_idx'] = []
        st.session_state['respostas'] = []
        st.session_state['cur_idx'] = 0
        st.session_state['nome'] = ''
        st.session_state['dificuldade'] = 'Medio'
        st.session_state['ranking'] = []

init_state()

# ---------------------------
# FUNÇÕES AUXILIARES
# ---------------------------
def iniciar_quiz():
    st.session_state['perguntas_idx'] = random.sample(range(len(QUESTOES)), len(QUESTOES))
    st.session_state['respostas'] = []
    st.session_state['cur_idx'] = 0
    st.session_state['iniciado'] = True
    st.session_state['finished'] = False

def registrar_resposta(valor):
    st.session_state['respostas'].append(valor)
    st.session_state['cur_idx'] += 1
    if st.session_state['cur_idx'] >= len(QUESTOES):
        st.session_state['finished'] = True

def calcular_categoria(total, max_pontos):
    p = total / max_pontos
    if p >= 0.85: return "Campeão Ambiental", "🏆"
    elif p >= 0.6: return "Protetor Verde", "🌿"
    elif p >= 0.4: return "Aprendiz Consciente", "🌱"
    else: return "Iniciante — Hora de Agir", "🌍"

# ---------------------------
# INTERFACE
# ---------------------------
st.markdown('<div class="main-card"><h1>🌎 Quiz Ambiental — Guardiões da Terra</h1><p class="small-muted">Teste seus hábitos e descubra seu nível de consciência ecológica.</p></div>', unsafe_allow_html=True)

if not st.session_state['iniciado'] and not st.session_state['finished']:
    st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
    if st.button("Iniciar Quiz 🌱"):
        iniciar_quiz()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state['iniciado'] and not st.session_state['finished']:
    idx = st.session_state['cur_idx']
    qidx = st.session_state['perguntas_idx'][idx]
    q = QUESTOES[qidx]
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    progresso = int(idx / len(QUESTOES) * 100)
    st.markdown(f"<h2>Pergunta {idx+1} de {len(QUESTOES)}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='progress-track'><div class='progress-fill' style='width:{progresso}%'></div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-card'><b>{q['q']}</b></div>", unsafe_allow_html=True)
    resposta = st.slider("Escolha sua resposta:", 1, 5, 3, key=f'q_{idx}')
    st.markdown(f"<div class='small-muted'>💡 {q['hint']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-muted'>🌍 {q['fact']}</div>", unsafe_allow_html=True)
    if st.button("Salvar resposta ✅"):
        st.markdown("<script>window.playGood();</script>", unsafe_allow_html=True)
        registrar_resposta(resposta)
        time.sleep(0.25)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state['finished']:
    respostas = st.session_state['respostas']
    total = sum(respostas)
    max_p = len(QUESTOES)*5
    categoria, emoji = calcular_categoria(total, max_p)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center'>{emoji} {categoria}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center'>Pontuação: <b>{total}</b> de {max_p}</p>", unsafe_allow_html=True)
    st.markdown("<script>window.launchConfetti();</script>", unsafe_allow_html=True)
    if st.button("🔁 Reiniciar Quiz"):
        st.session_state.clear()
        init_state()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
