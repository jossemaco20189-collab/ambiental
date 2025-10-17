import streamlit as st
import random
import time

# ======================================
# CONFIGURAÇÕES INICIAIS
# ======================================
st.set_page_config(
    page_title="Quiz Ambiental — Guardiões da Terra 🌍",
    page_icon="🌿",
    layout="wide"
)

# ======================================
# ESTILO PERSONALIZADO
# ======================================
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #e0f7e9, #aee1c9);
            font-family: 'Poppins', sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 38px;
            font-weight: bold;
            color: #1b5e20;
            margin-top: -20px;
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

# ======================================
# DADOS DO QUIZ
# ======================================
perguntas = [
    {
        "pergunta": "Qual dessas ações mais ajuda o meio ambiente?",
        "opcoes": ["Usar mais sacolas plásticas", "Separar o lixo reciclável", "Deixar luzes acesas"],
        "resposta": "Separar o lixo reciclável"
    },
    {
        "pergunta": "O que é mais sustentável?",
        "opcoes": ["Comprar garrafas plásticas", "Usar garrafa reutilizável", "Beber só refrigerante"],
        "resposta": "Usar garrafa reutilizável"
    },
    {
        "pergunta": "Qual é a principal causa do desmatamento?",
        "opcoes": ["Construção de casas", "Agricultura e pecuária", "Turismo"],
        "resposta": "Agricultura e pecuária"
    }
]

# ======================================
# ESTADOS DO APLICATIVO
# ======================================
if "fase" not in st.session_state:
    st.session_state["fase"] = "inicio"
if "indice" not in st.session_state:
    st.session_state_
