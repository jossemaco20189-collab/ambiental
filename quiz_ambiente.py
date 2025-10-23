# app.py
# Quiz Ambiental — Versão Pro (Streamlit)
# Rode: streamlit run app.py
# Autor: adaptado e aprimorado a partir do script fornecido pelo usuário.
# Objetivo: quiz imersivo, responsivo, com animações, sons e ranking.

import streamlit as st
import time
import random
import math
import json
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
# DADOS (QUESTÕES + FUN FACT POR PERGUNTA)
# ---------------------------
# Cada entrada tem: q, hint, fact (curiosidade ligada à pergunta)
QUESTOES = [
    {"q": "Evito jogar lixo em locais inadequados.",
     "hint": "Descartar corretamente evita entupimentos, poluição dos rios e prejuízo à fauna.",
     "fact": "O lixo que vai para rios costuma terminar no oceano — evitar descarte impróprio protege ecossistemas costeiros."},
    {"q": "Separo materiais recicláveis em casa.",
     "hint": "Separar facilita a reciclagem e reduz a extração de recursos naturais.",
     "fact": "Reciclar papel evita derrubada de árvores — uma tonelada de papel reciclado salva cerca de 17 árvores."},
    {"q": "Procuro reduzir o uso de plástico descartável.",
     "hint": "Plásticos descartáveis levam décadas ou séculos para se decompor.",
     "fact": "As microfibras plásticas já foram encontradas até em águas potáveis e peixes consumidos por humanos."},
    {"q": "Economizo água nas tarefas do dia a dia.",
     "hint": "Reduzir o tempo no banho e consertar vazamentos economiza milhares de litros por ano.",
     "fact": "Um vazamento pequeno pode desperdiçar mais de 200 litros por dia — conserte sempre que notar."},
    {"q": "Desligo luzes e aparelhos que não estão sendo usados.",
     "hint": "Desligar economiza energia e reduz emissões associadas à geração elétrica.",
     "fact": "Desligar um aparelho da tomada evita consumo fantasma — equipamentos em standby ainda gastam eletricidade."},
    {"q": "Participo ou apoio ações de preservação ambiental.",
     "hint": "A ação coletiva gera mudanças significativas em políticas e comportamento.",
     "fact": "Pequenas ações locais, como mutirões de limpeza, podem restaurar habitats e aumentar a biodiversidade local."},
    {"q": "Levo em conta o impacto ambiental ao comprar produtos.",
     "hint": "Escolher produtos com menos embalagem e maior durabilidade reduz resíduos.",
     "fact": "Produtos com certificações sustentáveis normalmente utilizam menos recursos de produção."},
    {"q": "Acredito que atitudes individuais ajudam o planeta.",
     "hint": "Atitudes somadas transformam mercados e políticas públicas.",
     "fact": "Campanhas de consumo consciente já mudaram práticas de empresas e reduziram embalagens."},
    {"q": "Procuro aprender mais sobre meio ambiente e biodiversidade.",
     "hint": "Conhecimento inspira ação e escolhas melhores no dia a dia.",
     "fact": "Comunidades educadas costumam alcançar melhores resultados em conservação e uso sustentável."},
    {"q": "Acho importante cobrar políticas públicas ambientais.",
     "hint": "Cobrança e participação influenciam legislações e fiscalizações.",
     "fact": "A pressão popular já foi decisiva para criação de áreas protegidas em muitos países."},
    {"q": "Uso transporte público ou bicicleta para reduzir emissões.",
     "hint": "Menos carros = menos emissões e menos congestionamento.",
     "fact": "Trocar trajetos curtos de carro por bicicleta reduz significativamente sua pegada de carbono anual."},
    {"q": "Planto árvores ou cuido de plantas em casa.",
     "hint": "Plantas ajudam a regular temperatura e limpar o ar localmente.",
     "fact": "Árvores maduras capturam toneladas de CO2 ao longo de décadas e melhoram ecossistemas urbanos."},
    {"q": "Evito o desperdício de alimentos no meu dia a dia.",
     "hint": "Planejar refeições e armazenar corretamente reduz desperdício e emissões.",
     "fact": "Um terço do alimento produzido no mundo é desperdiçado — reduzir desperdício ajuda recursos e clima."}
]

# ---------------------------
# ESTILO GLOBAL (CSS + JS) — VERSÃO APRIMORADA COM DARK MODE
# ---------------------------
# Comentários: estilo moderno, responsivo, com animações e suporte a dark mode.
st.markdown(
    """
    <style>
    :root{
        --bg-start: #e9fff4;
        --bg-end: #e0f7fb;
        --card: rgba(255,255,255,0.98);
        --accent: #2e8b57;
        --muted: #2f6b3f;
        --gold: #ffd36b;
        --text: #05321a;
        --muted-contrast: #4d6b56;
    }
    html, body { background: linear-gradient(180deg, var(--bg-start), var(--bg-end)); color: var(--text); }
    .main-card{
        background: var(--card);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(20,80,40,0.06);
        margin-bottom: 18px;
        color: var(--text) !important;
    }
    .header-row{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
    .planet{ width:92px; height:92px; border-radius:50%; background: radial-gradient(circle at 35% 35%, #79c68b, var(--accent)); box-shadow: 0 8px 20px rgba(30,80,40,0.12); animation: spinPlanet 18s linear infinite; display:flex; align-items:center; justify-content:center; font-size:34px; color: #fff; }
    @keyframes spinPlanet{ from{ transform: rotate(0deg)} to{ transform: rotate(360deg)} }
    h1 { color: var(--accent); margin-bottom:6px; }
    h2 { color: var(--accent); }
    .question-card{ border-left:6px solid var(--accent); padding:14px; border-radius:10px; margin-bottom:12px; background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,255,250,0.9)); color:var(--text) !important; }
    .small-muted{ color:var(--muted-contrast); opacity:0.95; font-size:14px; }
    .badge { background: linear-gradient(90deg,var(--gold),#ff9a3c); padding:6px 10px; border-radius:999px; font-weight:600; color:#2b2b2b; }
    .btn-green{ background: linear-gradient(90deg,#4cd964,#2e8b57); color:white; padding:10px 14px; border-radius:10px; border:none; cursor:pointer; }
    .center { display:flex; justify-content:center; align-items:center; }
    .confetti-canvas{ position:fixed; left:0; top:0; width:100%; height:100%; pointer-events:none; z-index:9999; }
    .avatar { width:72px; height:72px; border-radius:12px; background: linear-gradient(180deg,#e4fff0,#d6f6e8); display:flex; align-items:center; justify-content:center; font-size:32px; color:var(--accent); box-shadow: 0 6px 16px rgba(40,100,60,0.06); }
    .progress-track{ background:#e6f7ee; border-radius:12px; padding:4px; }
    .progress-fill{ height:12px; border-radius:8px; background: linear-gradient(90deg,#7bf28a,#2e8b57); width:0%; transition: width 700ms ease; }

    /* Force legible color for form controls and buttons (override Streamlit dark rules) */
    input, textarea, select, button, .stSlider, .stTextInput, .stTextArea {
        color: var(--text) !important;
    }
    input::placeholder, textarea::placeholder { color: #7d9a87 !important; }

    /* responsive tweaks */
    @media (max-width: 800px){
        .planet{ width:72px; height:72px; font-size:26px; }
        .avatar{ width:56px; height:56px; font-size:24px; }
    }

    /* --- DARK MODE OVERRIDES --- */
    @media (prefers-color-scheme: dark) {
        :root{
            --bg-start: #071411;
            --bg-end: #0b1f1a;
            --card: rgba(12,20,18,0.9);
            --accent: #7bd389;
            --muted: #a7cbb3;
            --gold: #ffc96b;
            --text: #e6fff2;
            --muted-contrast: #bcdcc5;
        }
        html, body { background: linear-gradient(180deg, var(--bg-start), var(--bg-end)); color: var(--text) !important; }
        .main-card{ background: var(--card) !important; box-shadow: 0 8px 28px rgba(0,0,0,0.6); color: var(--text) !important; }
        .question-card{ background: linear-gradient(180deg, rgba(20,30,26,0.75), rgba(12,20,16,0.6)) !important; border-left-color: var(--accent) !important; color: var(--text) !important; }
        h1, h2 { color: var(--accent) !important; }
        .small-muted{ color: var(--muted-contrast) !important; opacity:0.95; }
        .badge{ color:#1a1a1a !important; background: linear-gradient(90deg,var(--gold),#ff9a3c) !important; }
        .avatar { background: linear-gradient(180deg,#08322a,#0a2b22) !important; color: var(--accent) !important; box-shadow: 0 6px 16px rgba(0,0,0,0.6); }
        .progress-track{ background: rgba(255,255,255,0.03) !important; }
        .progress-fill{ background: linear-gradient(90deg,#2bd47a,var(--accent)) !important; }

        /* Inputs, sliders, buttons legíveis no escuro */
        input, textarea, select, button, .stSlider, .stTextInput, .stTextArea {
            color: var(--text) !important;
            background: rgba(255,255,255,0.02) !important;
            border-color: rgba(255,255,255,0.06) !important;
        }
        input::placeholder, textarea::placeholder { color: rgba(255,255,255,0.5) !important; }

        /* Forçar contraste em labels/legendas */
        label, .css-1kyxreq, .css-1outpf7, .css-1lcbugb { color: var(--text) !important; }
    }
    </style>

    <script>
    // WebAudio short sounds (positive/negative/ambient)
    window.playGood = function(){ try{ const ctx = new (window.AudioContext||window.webkitAudioContext)(); const o = ctx.createOscillator(); const g = ctx.createGain(); o.type = 'sine'; o.frequency.value = 880; g.gain.value = 0.04; o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.12); }catch(e){} };
    window.playBad = function(){ try{ const ctx = new (window.AudioContext||window.webkitAudioContext)(); const o = ctx.createOscillator(); const g = ctx.createGain(); o.type = 'triangle'; o.frequency.value = 220; g.gain.value = 0.06; o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.22); }catch(e){} };
    window.playApplause = function(){ try{ const ctx = new (window.AudioContext||window.webkitAudioContext)(); const o = ctx.createOscillator(); const g = ctx.createGain(); o.type = 'sawtooth'; o.frequency.value = 620; g.gain.value = 0.02; o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.2); }catch(e){} };

    // Confetti basic - creates small colored divs and animates them
    window.launchConfetti = function(){ const colors = ['#ff6b6b','#ffd93d','#6bf178','#6bbcff','#b86bff']; for(let i=0;i<80;i++){ const el = document.createElement('div'); el.style.position='fixed'; el.style.left=(Math.random()*100)+'%'; el.style.top='-5%'; el.style.width=(6+Math.random()*6)+'px'; el.style.height=(10+Math.random()*10)+'px'; el.style.background=colors[Math.floor(Math.random()*colors.length)]; el.style.opacity='0.95'; el.style.transform='rotate('+Math.random()*360+'deg)'; el.style.zIndex=9999; el.style.borderRadius='2px'; el.style.transition='transform 3s linear, top 3s linear, left 3s linear, opacity 3s linear'; document.body.appendChild(el); setTimeout(()=>{ el.style.top=(80+Math.random()*20)+'%'; el.style.left=(Math.random()*100)+'%'; el.style.transform='translateY(0) rotate('+Math.random()*720+'deg)'; el.style.opacity='0'; },20); setTimeout(()=>el.remove(),3500); } };
    </script>
    """, unsafe_allow_html=True
)

# ---------------------------
# UTILITÁRIOS DE ESTADO / RANKING
# ---------------------------
def init_state():
    """Inicializa chaves de session_state usadas no app."""
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
        st.session_state['iniciado'] = False
        st.session_state['finished'] = False
        st.session_state['perguntas_idx'] = []
        st.session_state['respostas'] = []
        st.session_state['cur_idx'] = 0
        st.session_state['start_time'] = None
        st.session_state['dificuldade'] = 'Medio'
        st.session_state['nome'] = ''
        st.session_state['ranking'] = []  # guardado apenas em session por enquanto
        st.session_state['show_ambient_sound'] = False
        st.session_state['avatar'] = '🌱'

init_state()

def carregar_ranking_local():
    """Retorna ranking guardado na session_state (simulação local)."""
    return st.session_state.get('ranking', [])

def salvar_no_ranking_local(nome, pontos):
    """Salva no ranking local (session_state)."""
    r = carregar_ranking_local()
    r.append({"nome": nome, "pontos": pontos, "ts": datetime.utcnow().isoformat()})
    r.sort(key=lambda x: x['pontos'], reverse=True)
    st.session_state['ranking'] = r[:50]

# ---------------------------
# FUNÇÕES AUXILIARES DE QUIZ
# ---------------------------
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

def iniciar_quiz(dificuldade='Medio'):
    """Prepara o quiz (embaralha perguntas, reseta estado)."""
    perguntas_idx = list(range(len(QUESTOES)))
    random.shuffle(perguntas_idx)
    st.session_state['perguntas_idx'] = perguntas_idx
    st.session_state['respostas'] = []
    st.session_state['cur_idx'] = 0
    st.session_state['iniciado'] = True
    st.session_state['finished'] = False
    st.session_state['start_time'] = time.time()
    st.session_state['dificuldade'] = dificuldade

def registrar_resposta(valor):
    """Registra resposta e avança para próxima pergunta."""
    st.session_state['respostas'].append(valor)
    st.session_state['cur_idx'] += 1
    if st.session_state['cur_idx'] >= len(QUESTOES):
        st.session_state['finished'] = True

# ---------------------------
# UI: SIDEBAR (CONFIGURAÇÕES)
# ---------------------------
with st.sidebar:
    st.markdown("<div style='padding:10px'><h3 style='margin:0'>⚙️ Configurações</h3></div>", unsafe_allow_html=True)
    st.session_state['nome'] = st.text_input("Seu nome (opcional)", value=st.session_state.get('nome',''))
    st.session_state['avatar'] = st.selectbox("Escolha um avatar", options=['🌱','🦊','🐦','🌳','🐢'], index=0)
    st.session_state['dificuldade'] = st.selectbox("Nível de dificuldade", options=['Facil','Medio','Dificil'], index=1)
    st.session_state['show_ambient_sound'] = st.checkbox("Música/ambiente sonora (opcional)", value=False)
    if st.session_state['show_ambient_sound']:
        st.markdown("<div class='small-muted' style='margin-top:6px'>Se quiser música ambiente, defina a URL em AMBIENT_AUDIO_URL no código.</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🏅 Ranking")
    ranking = carregar_ranking_local()
    if ranking:
        for i, item in enumerate(ranking[:8], start=1):
            st.write(f"{i}. {item['nome'] or 'Anônimo'} — {item['pontos']} pts")
    else:
        st.write("Seja o primeiro a marcar pontos
