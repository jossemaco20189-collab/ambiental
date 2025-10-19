# app.py
# Quiz Ambiental — Versão Pro (Streamlit)
# (apenas a escala foi atualizada para “Nunca faço isso → Sempre”)

import streamlit as st
import time
import random
import math
import json
from datetime import datetime

st.set_page_config(
    page_title="Quiz Ambiental — Guardiões da Terra",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# (CSS, JS, utilitários e funções mantidos 100% iguais — sem mudanças)

# --- (pulei até a parte onde aparecem as instruções e o slider) ---

# BOTÕES INICIAIS
if not st.session_state['iniciado'] and not st.session_state['finished']:
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("Iniciar quiz 🌱"):
            iniciar_quiz(st.session_state['dificuldade'])
            st.rerun()
    with col2:
        if st.button("Ver instruções ⓘ"):
            st.info(
                "Responda cada pergunta em escala de 1️⃣ (nunca faço isso) a 5️⃣ (sempre). "
                "Ao salvar, você verá feedback animado e uma dica relacionada."
            )
    with col3:
        if st.button("Exibir perguntas (modo rápido)"):
            st.session_state['modo_rapido'] = True

# --- MODO RÁPIDO (todas perguntas) ---
if st.session_state.get('modo_rapido'):
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Modo Rápido: responda todas as perguntas")
    respostas_fast = []
    for i, quest in enumerate(QUESTOES, start=1):
        st.markdown(f"**{i}. {quest['q']}**")
        val = st.slider(
            "Selecione:",
            1, 5, 3,
            key=f'fast_{i}',
            help='1️⃣ Nunca faço isso ... 5️⃣ Sempre'
        )
        st.markdown(f"<div class='small-muted'>Dica: {quest['hint']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted'>Fun Fact: {quest['fact']}</div>", unsafe_allow_html=True)
        respostas_fast.append(val)

# --- QUIZ (uma pergunta por vez) ---
if st.session_state['iniciado'] and not st.session_state['finished']:
    idx = st.session_state['cur_idx']
    perguntas_idx = st.session_state['perguntas_idx']
    qidx = perguntas_idx[idx]
    pergunta = QUESTOES[qidx]
    container = st.empty()
    with container.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        progresso_pct = int(((idx) / len(QUESTOES)) * 100)
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:center'>"
            f"<div><h2>Pergunta {idx+1} de {len(QUESTOES)}</h2></div>"
            f"<div style='width:45%'><div class='progress-track'>"
            f"<div class='progress-fill' style='width:{progresso_pct}%'></div>"
            f"</div></div></div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<div class='question-card'><b>{pergunta['q']}</b></div>", unsafe_allow_html=True)

        col_main_q, col_side_q = st.columns([3,1])
        with col_main_q:
            resposta = st.slider(
                "Escolha sua resposta:",
                1, 5, 3,
                key=f'q_{idx}',
                help='1️⃣ Nunca faço isso ... 5️⃣ Sempre'
            )
            st.markdown(f"<div class='small-muted'>Dica: {pergunta['hint']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='small-muted'>Fun Fact: {pergunta['fact']}</div>", unsafe_allow_html=True)
