import streamlit as st
import random
import time

# ==============================
# CONFIGURAÇÕES DO APP
# ==============================
st.set_page_config(
    page_title="Quiz Ambiental — Guardiões da Terra 🌍",
    page_icon="🌿",
    layout="wide"
)

# ==============================
# ESTILOS PERSONALIZADOS
# ==============================
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #e8f5e9, #a5d6a7);
            font-family: 'Poppins', sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 40px;
            color: #1b5e20;
            font-weight: 700;
            margin-bottom: -5px;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #2e7d32;
            margin-bottom: 40px;
        }
        .stButton>button {
            background-color: #43a047 !important;
            color: white !important;
            border-radius: 12px;
            padding: 10px 25px;
            font-size: 18px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #2e7d32 !important;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# BANCO DE PERGUNTAS (1 a 3)
# ==============================
perguntas = [
    {
        "pergunta": "1️⃣ Qual dessas ações mais ajuda o meio ambiente?",
        "opcoes": ["Usar sacolas plásticas", "Separar o lixo reciclável", "Deixar luzes acesas"],
        "resposta": "Separar o lixo reciclável"
    },
    {
        "pergunta": "2️⃣ O que é mais sustentável?",
        "opcoes": ["Comprar garrafas plásticas", "Usar garrafa reutilizável", "Beber só refrigerante"],
        "resposta": "Usar garrafa reutilizável"
    },
    {
        "pergunta": "3️⃣ Qual é a principal causa do desmatamento?",
        "opcoes": ["Construção de casas", "Agricultura e pecuária", "Turismo"],
        "resposta": "Agricultura e pecuária"
    }
]

# ==============================
# ESTADOS DO APLICATIVO
# ==============================
if "fase" not in st.session_state:
    st.session_state["fase"] = "inicio"
if "indice" not in st.session_state:
    st.session_state["indice"] = 0
if "pontos" not in st.session_state:
    st.session_state["pontos"] = 0
if "musica_tocando" not in st.session_state:
    st.session_state["musica_tocando"] = False

# ==============================
# FUNÇÕES AUXILIARES
# ==============================
def reiniciar_quiz():
    st.session_state["fase"] = "inicio"
    st.session_state["indice"] = 0
    st.session_state["pontos"] = 0
    st.session_state["musica_tocando"] = False
    st.rerun()

# ==============================
# CABEÇALHO
# ==============================
st.markdown("<h1 class='main-title'>Quiz Ambiental — Guardiões da Terra 🌎</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Descubra o quanto você sabe sobre o meio ambiente e ajude a preservar o planeta!</p>", unsafe_allow_html=True)

# ==============================
# INÍCIO
# ==============================
if st.session_state["fase"] == "inicio":
    if st.button("🌿 Iniciar Quiz"):
        st.session_state["fase"] = "quiz"
        st.session_state["indice"] = 0
        st.session_state["pontos"] = 0
        st.session_state["musica_tocando"] = True
        st.rerun()

# ==============================
# MÚSICA DE FUNDO (após começar)
# ==============================
if st.session_state["musica_tocando"]:
    st.markdown("""
        <audio autoplay loop>
            <source src="https://cdn.pixabay.com/download/audio/2021/11/03/audio_8e6c17a2e2.mp3?filename=forest-nature-sound-ambient-ambient-110997.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

# ==============================
# FASE DO QUIZ
# ==============================
if st.session_state["fase"] == "quiz":
    idx = st.session_state["indice"]

    # ✅ Correção de índice fora do limite
    if idx < len(perguntas):
        pergunta_atual = perguntas[idx]
    else:
        st.session_state["fase"] = "resultado"
        st.rerun()
        st.stop()

    st.subheader(f"🍃 Pergunta {idx + 1} de {len(perguntas)}")
    st.write(f"**{pergunta_atual['pergunta']}**")

    opcao = st.radio("Escolha sua resposta:", pergunta_atual["opcoes"], key=f"resposta_{idx}")

    if st.button("Responder"):
        if opcao == pergunta_atual["resposta"]:
            st.success("✅ Resposta certa! Excelente!")
            st.balloons()  # 🎉 Efeito de confete a cada acerto
            st.session_state["pontos"] += 1
        else:
            st.error(f"❌ Resposta errada! A correta era: {pergunta_atual['resposta']}")

        time.sleep(1.5)

        if idx + 1 < len(perguntas):
            st.session_state["indice"] += 1
            st.rerun()
        else:
            st.session_state["fase"] = "resultado"
            st.rerun()

# ==============================
# RESULTADO FINAL
# ==============================
if st.session_state["fase"] == "resultado":
    st.balloons()
    total = len(perguntas)
    pontos = st.session_state["pontos"]

    # ✅ Correção para evitar erro sem resposta
    if total == 0:
        st.warning("Responda pelo menos uma pergunta antes de finalizar 🌱")
        st.stop()

    st.success(f"🎉 Você acertou {pontos} de {total} perguntas!")

    if pontos == total:
        st.write("🌎 Incrível! Você é um verdadeiro Guardião da Terra!")
    elif pontos >= total / 2:
        st.write("🍃 Muito bem! Você entende bastante sobre o meio ambiente.")
    else:
        st.write("💧 Continue aprendendo, o planeta precisa de você!")

    st.button("🔄 Jogar novamente", on_click=reiniciar_quiz)
