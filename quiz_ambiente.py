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
# ESTILO GLOBAL (CSS + JS)
# ---------------------------
# Comentários: estilo moderno, responsivo e com animações.
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
    }
    html, body { background: linear-gradient(180deg, var(--bg-start), var(--bg-end)); }
    .main-card{
        background: var(--card);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(20,80,40,0.06);
        margin-bottom: 18px;
    }
    .header-row{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
    .planet{ width:92px; height:92px; border-radius:50%; background: radial-gradient(circle at 35% 35%, #79c68b, var(--accent)); box-shadow: 0 8px 20px rgba(30,80,40,0.12); animation: spinPlanet 18s linear infinite; display:flex; align-items:center; justify-content:center; font-size:34px; color: #fff; }
    @keyframes spinPlanet{ from{ transform: rotate(0deg)} to{ transform: rotate(360deg)} }
    h1 { color: var(--accent); margin-bottom:6px; }
    h2 { color: var(--accent); }
    .question-card{ border-left:6px solid var(--accent); padding:14px; border-radius:10px; margin-bottom:12px; background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,255,250,0.9));}
    .small-muted{ color:var(--muted); opacity:0.9; font-size:14px; }
    .badge { background: linear-gradient(90deg,var(--gold),#ff9a3c); padding:6px 10px; border-radius:999px; font-weight:600; }
    .btn-green{ background: linear-gradient(90deg,#4cd964,#2e8b57); color:white; padding:10px 14px; border-radius:10px; border:none; cursor:pointer; }
    .center { display:flex; justify-content:center; align-items:center; }
    .confetti-canvas{ position:fixed; left:0; top:0; width:100%; height:100%; pointer-events:none; z-index:9999; }
    .avatar { width:72px; height:72px; border-radius:12px; background: linear-gradient(180deg,#e4fff0,#d6f6e8); display:flex; align-items:center; justify-content:center; font-size:32px; color:var(--accent); box-shadow: 0 6px 16px rgba(40,100,60,0.06); }
    .progress-track{ background:#e6f7ee; border-radius:12px; padding:4px; }
    .progress-fill{ height:12px; border-radius:8px; background: linear-gradient(90deg,#7bf28a,#2e8b57); width:0%; transition: width 700ms ease; }
    /* responsive tweaks */
    @media (max-width: 800px){
        .planet{ width:72px; height:72px; font-size:26px; }
        .avatar{ width:56px; height:56px; font-size:24px; }
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
        st.write("Seja o primeiro a marcar pontos!")

# ---------------------------
# TELA INICIAL / HEADER
# ---------------------------
col_main, col_aside = st.columns([3,1])
with col_main:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="header-row">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;flex-direction:column;gap:4px">', unsafe_allow_html=True)
    st.markdown('<h1>Quiz Ambiental — Guardiões da Terra 🌎</h1>', unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Teste seus hábitos, aprenda com dicas por pergunta e mostre seu nível de proteção ambiental.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;flex-direction:column;align-items:center;gap:8px'><div class='planet' title='Planeta Guardião'>🌍</div><div class='small-muted'>Planeta Guardião</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_aside:
    st.markdown('<div class="main-card" style="text-align:center">', unsafe_allow_html=True)
    st.markdown(f"<div class='avatar'>{st.session_state['avatar']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-top:8px; font-weight:600'>{st.session_state.get('nome') or 'Visitante'}</div>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Seu guia: EcoBot 🌿</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")  # espaçamento

# ---------------------------
# BOTÕES INICIAIS (se ainda não iniciou)
# ---------------------------
if not st.session_state['iniciado'] and not st.session_state['finished']:
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("Iniciar quiz 🌱"):
            iniciar_quiz(st.session_state['dificuldade'])
            st.rerun()
    with col2:
        if st.button("Ver instruções ⓘ"):
            st.info("Responda cada pergunta em escala de 1 (Nunca faço isso) a 5 (Sempre faço isso). Ao salvar, você verá feedback animado e uma dica relacionada.")
    with col3:
        if st.button("Exibir perguntas (modo rápido)"):
            # abrir modo rápido abaixo (fallback)
            st.session_state['modo_rapido'] = True

# ---------------------------
# EXIBIÇÃO: MODO RÁPIDO (TODAS PERGUNTAS)
# ---------------------------
if st.session_state.get('modo_rapido'):
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Modo Rápido: responda todas as perguntas")
    respostas_fast = []
    for i, quest in enumerate(QUESTOES, start=1):
        st.markdown(f"**{i}. {quest['q']}**")
        val = st.slider("", 1, 5, 3, key=f'fast_{i}')
        st.markdown(f"<div class='small-muted'>Dica: {quest['hint']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted'>Fun Fact: {quest['fact']}</div>", unsafe_allow_html=True)
        respostas_fast.append(val)
    if st.button("Ver Resultado (modo rápido)"):
        total = sum(respostas_fast)
        max_p = len(QUESTOES) * 5
        categoria, emoji = calcular_categoria(total, max_p)
        st.success(f"{emoji} {categoria} — {total}/{max_p}")
        salvar_no_ranking_local(st.session_state.get('nome') or 'Anônimo', total)
        st.session_state['modo_rapido'] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# TELA DO QUIZ (UMA PERGUNTA POR VEZ)
# ---------------------------
if st.session_state['iniciado'] and not st.session_state['finished']:
    idx = st.session_state['cur_idx']
    perguntas_idx = st.session_state['perguntas_idx']
    # proteção caso algo dê errado com indices
    if idx < 0: idx = 0
    if idx >= len(QUESTOES):
        st.session_state['finished'] = True
        st.rerun()

    qidx = perguntas_idx[idx]
    pergunta = QUESTOES[qidx]

    # container que facilita animações/transições
    container = st.empty()
    with container.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        progresso_pct = int(((idx) / len(QUESTOES)) * 100)
        # header pergunta + progresso
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:center'><div><h2>Pergunta {idx+1} de {len(QUESTOES)}</h2><div class='small-muted'>Nível: <span class='badge'>{st.session_state['dificuldade']}</span></div></div><div style='width:45%'><div class='progress-track'><div class='progress-fill' style='width:{progresso_pct}%'></div></div></div></div>",
            unsafe_allow_html=True)
        st.markdown(f"<div class='question-card'><b>{pergunta['q']}</b></div>", unsafe_allow_html=True)

        col_main_q, col_side_q = st.columns([3,1])
        with col_main_q:
            # pergunta: slider 1-5 (1=discordo totalmente ... 5=concordo totalmente)
            resposta = st.slider("Escolha sua resposta:", 1, 5, 3, key=f'q_{idx}', help='1 = Discordo totalmente ... 5 = Concordo totalmente')
            st.markdown(f"<div class='small-muted'>Dica: {pergunta['hint']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='small-muted'>Fun Fact: {pergunta['fact']}</div>", unsafe_allow_html=True)
        with col_side_q:
            st.markdown('<div style="display:flex;flex-direction:column;gap:10px;align-items:stretch">', unsafe_allow_html=True)
            if st.button("✅ Salvar resposta"):
                # feedback visual/sonoro
                if resposta >= 4:
                    # bom
                    st.markdown("<script>window.playGood();</script>", unsafe_allow_html=True)
                    st.success("Boa! Ação positiva registrada ✅")
                else:
                    st.markdown("<script>window.playBad();</script>", unsafe_allow_html=True)
                    st.warning("Obrigado! Essa é uma boa área para melhoria ❗")
                # registrar e avançar
                registrar_resposta(resposta)
                # pequeno delay para percepção do usuário e animação
                time.sleep(0.25)
                # avançar - rerun atualiza a tela
                st.rerun()

            if st.button("💡 Dica extra"):
                st.info("Pequena ação: comece com 1 hábito novo esta semana — por exemplo, levar sua garrafa reutilizável.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# RESULTADO FINAL
# ---------------------------
if st.session_state['finished']:
    # calcula total
    respostas = st.session_state.get('respostas', [])
    total = sum(respostas)
    max_p = len(QUESTOES) * 5
    categoria, emoji = calcular_categoria(total, max_p)

    # cartão resultado final
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header('📊 Resultado Final')
    st.markdown(f"<h2 style='text-align:center'>{emoji} {categoria}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:18px'>Pontuação: <b>{total}</b> de {max_p}</p>", unsafe_allow_html=True)

    # animação de contagem simples (visual apenas)
    with st.spinner('Gerando seus insights...'):
        for i in range(12):
            time.sleep(0.03)
    st.success('Pronto! Veja abaixo suas recomendações personalizadas 🌱')

    # recomendações personalizadas baseadas na média
    media = total / len(QUESTOES)
    dicas = []
    if media < 2.5:
        dicas.append('Recomendo focar em reduzir desperdício e economizar água: pequenas metas semanais ajudam muito.')
        dicas.append('Tente anotar 3 ações práticas que você pode começar esta semana (ex: reduzir plástico descartável).')
    elif media < 4:
        dicas.append('Você está indo bem! Compartilhe práticas com amigos e familiares para ampliar o impacto.')
        dicas.append('Procure projetos locais (plantio, limpeza de rios) para participar e aprender mais.')
    else:
        dicas.append('Excelente! Considere engajar-se em ações de liderança comunitária ou projetos locais.')
        dicas.append('Pense em como apoiar políticas públicas e iniciativas maiores na sua região.')

    dicas.append('Dica prática: reduzir o desperdício de alimentos e consertar vazamentos tem alto retorno ambiental.')

    st.markdown('<ul>', unsafe_allow_html=True)
    for d in dicas:
        st.markdown(f"<li class='small-muted'>{d}</li>", unsafe_allow_html=True)
    st.markdown('</ul>', unsafe_allow_html=True)

    # botões de ação final
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button('🎉 Celebrar — Confete e som'):
            # confete + som
            st.markdown("<script>window.launchConfetti(); window.playApplause();</script>", unsafe_allow_html=True)
            st.success("Parabéns! 🎊")
    with col2:
        if st.button('🔁 Reiniciar quiz (suave)'):
            # limpa estado mantendo nome/dificuldade
            nome = st.session_state.get('nome','')
            dificuldade = st.session_state.get('dificuldade','Medio')
            avatar = st.session_state.get('avatar','🌱')
            st.session_state.clear()
            # re-inicializa e restaura algumas preferências para melhor UX
            init_state()
            st.session_state['nome'] = nome
            st.session_state['dificuldade'] = dificuldade
            st.session_state['avatar'] = avatar
            st.rerun()
    with col3:
        if st.button('💾 Salvar no ranking'):
            salvar_no_ranking_local(st.session_state.get('nome') or 'Anônimo', total)
            st.success('Salvo! Veja no painel lateral.')

    # mini share text (copiar)
    share_text = f"Fiz o Quiz Ambiental e tirei {total}/{max_p} — participe também e proteja o planeta! 🌍"
    st.markdown(f"<div style='display:flex;gap:8px;align-items:center'><input style='flex:1;padding:8px;border-radius:8px;border:1px solid #ddd' value='{share_text}' id='sharetxt' readonly><button onclick='navigator.clipboard.writeText(document.getElementById(\"sharetxt\").value)' style='padding:8px;border-radius:8px;margin-left:8px'>Copiar</button></div>", unsafe_allow_html=True)

    # salva automaticamente no ranking local para conveniência (uma vez)
    if not st.session_state.get('saved_to_ranking'):
        salvar_no_ranking_local(st.session_state.get('nome') or 'Anônimo', total)
        st.session_state['saved_to_ranking'] = True

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# RODAPÉ / CONTROLES ADICIONAIS
# ---------------------------
st.markdown("<div style='margin-top:20px; text-align:center; color:var(--muted)'>Desenvolvido como ferramenta educativa — personalize para sua escola, feira de ciências ou portfólio.</div>", unsafe_allow_html=True)

# ---------------------------
# AMBIENT AUDIO (opcional)
# ---------------------------
# Se quiser música ambiente, defina a URL do arquivo MP3 abaixo e descomente a injeção HTML.
AMBIENT_AUDIO_URL = None
# Exemplo (se tiver mp3 hospedado): AMBIENT_AUDIO_URL = "https://your-hosted-audio/forest_ambient.mp3"
if st.session_state['show_ambient_sound'] and AMBIENT_AUDIO_URL:
    st.markdown(f"""
    <audio autoplay loop>
      <source src="{AMBIENT_AUDIO_URL}" type="audio/mpeg">
      Seu navegador não suporta áudio incorporado.
    </audio>
    """, unsafe_allow_html=True)

# ---------------------------
# NOTAS FINAIS / COMENTÁRIOS (para desenvolvedor)
# ---------------------------
# - O app mantém toda a lógica de pergunta por pergunta e modo rápido.
# - Fun facts agora são específicos por pergunta (campo 'fact' em cada questão).
# - Use 'salvar_no_ranking_local' para persistir apenas em session_state; se desejar persistir em arquivo/BD,
#   implemente leitura/escrita (CSV/JSON) ou use um storage na nuvem.
# - Sons usam WebAudio API (sem arquivos). Se quiser sons mais ricos, hospede arquivos .mp3 e adicione <audio>.
# - Confete e efeitos são feitos via DOM (JS) para evitar bibliotecas externas.
# - Widgets re-renderizam com st.rerun() (compatível com Streamlit atual).
#
# Se quiser, eu:
# - Adiciono persistência em JSON/CSV no servidor (para ranking permanente).
# - Faço exportação do resultado para PDF ou slides.
# - Ajusto cores/tema para combinar com identidade visual da sua apresentação.
#
# Pronto — quer que eu adapte o layout para um tema específico (ex: cores da sua escola) ou
# adicione um logotipo no topo?
