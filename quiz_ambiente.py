import streamlit as st
import random
import time

# 🌿 Configuração da página
st.set_page_config(
    page_title="Quiz Ambiental — Guardiões da Terra 🌎",
    page_icon="🌱",
    layout="wide"
)

# =======================
# CSS ESTILIZADO
# =======================
st.markdown("""
    <style>
    body {
        background: linear-gradient(180deg, #e2f4e8, #b8e4c9);
        font-family: 'Segoe UI', sans-serif;
        color: #1b4332;
    }
    .main {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0px 0px 25px rgba(0, 100, 0, 0.3);
        animation: fadeIn 1s ease;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    h1, h2 {
        text-align: center;
        color: #2b7a0b;
    }
    .question-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 6px solid #4CAF50;
        transition: 0.3s;
    }
    .question-card:hover {
        transform: scale(1.03);
        background-color: #eaffea;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #2e8b57);
        color: white;
        font-size: 18px;
        padding: 15px 35px;
        border-radius: 15px;
        border: none;
        transition: 0.3s;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    .stButton>button:hover {
        transform: scale(1.08);
    }
    .progress-bar {
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .progress-bar-fill {
        height: 25px;
        background: linear-gradient(90deg, #4CAF50, #2e8b57);
        width: 0;
        transition: width 0.5s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# =======================
# FUN FACTS
# =======================
fun_facts = [
    "🌳 Plantar árvores ajuda a combater o aquecimento global – cada árvore absorve CO₂!",
    "♻️ Reciclar uma lata de alumínio economiza energia suficiente para ouvir rádio por 3 horas.",
    "💧 Reduzir o desperdício de comida pode economizar água suficiente para 50 piscinas olímpicas por dia.",
    "🌍 Pequenas atitudes geram grandes mudanças para o planeta!",
]

# =======================
# PERGUNTAS DO QUIZ
# =======================
perguntas = [
    "Evito jogar lixo em locais inadequados.",
    "Separo materiais recicláveis em casa.",
    "Procuro reduzir o uso de plástico descartável.",
    "Economizo água nas tarefas do dia a dia.",
    "Desligo luzes e aparelhos que não estão sendo usados.",
    "Participo ou apoio ações de preservação ambiental.",
    "Levo em conta o impacto ambiental ao comprar produtos.",
    "Acredito que atitudes individuais ajudam o planeta.",
    "Procuro aprender mais sobre meio ambiente e biodiversidade.",
    "Acho importante cobrar políticas públicas ambientais.",
    "Uso transporte público ou bicicleta para reduzir emissões.",
    "Planto árvores ou cuido de plantas em casa.",
    "Evito o desperdício de alimentos no meu dia a dia."
]

# =======================
# FUNÇÕES PRINCIPAIS
# =======================
def tela_inicio():
    st.markdown("## Quiz Ambiental — Guardiões da Terra 🌎")
    st.markdown("Teste seus hábitos e descubra o quão preparado você está para proteger o meio ambiente. Um quiz educativo, bonito e com feedbacks imediatos.")

    col1, col2 = st.columns([1, 2])
    with col1:
        nome = st.text_input("Seu nome (opcional)")
        dificuldade = st.selectbox("Nível de dificuldade", ["Fácil", "Médio", "Difícil"], index=1)
        som = st.checkbox("🔊 Habilitar sons curtos (WebAudio)")
        dicas = st.checkbox("💡 Mostrar dicas educativas após cada pergunta")

        if st.button("Iniciar quiz 🍃"):
            st.session_state.update({
                "quiz_iniciado": True,
                "indice_pergunta": 0,
                "respostas": [],
                "nome": nome,
                "som": som,
                "dicas": dicas,
                "dificuldade": dificuldade
            })
            st.rerun()

def exibir_pergunta():
    idx = st.session_state["indice_pergunta"]

    if idx >= len(perguntas):
        st.session_state["fase"] = "resultado"
        st.rerun()

    pergunta = perguntas[idx]
    st.markdown(f"### 🌿 Pergunta {idx + 1} de {len(perguntas)}")
    st.markdown(f"<div class='question-card'><b>{pergunta}</b></div>", unsafe_allow_html=True)

    resposta = st.slider("Selecione uma opção:", 1, 5, 3, key=f"resposta_{idx}")
    if st.button("Próxima pergunta ➡️"):
        st.session_state["respostas"].append(resposta)
        st.session_state["indice_pergunta"] += 1
        st.rerun()

    if st.session_state["dicas"]:
        st.info(random.choice(fun_facts))

    progresso = (idx / len(perguntas)) * 100
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {progresso}%;"></div>
        </div>
    """, unsafe_allow_html=True)

def exibir_resultado():
    respostas = st.session_state.get("respostas", [])
    if not respostas:
        st.warning("⚠️ Você precisa responder pelo menos uma pergunta antes de ver o resultado.")
        return

    total = sum(respostas)
    max_pontos = len(perguntas) * 5
    proporcao = total / max_pontos

    st.markdown("## 📊 Resultado Final")
    st.markdown(f"**Pontuação:** {total} / {max_pontos}")

    if proporcao >= 0.85:
        st.success("🏆 Excelente! Você é um verdadeiro Guardião da Terra! 🌍")
    elif proporcao >= 0.6:
        st.info("🍃 Muito bom! Suas atitudes já ajudam o planeta, continue assim!")
    else:
        st.warning("🌱 Hora de agir! Comece com pequenas mudanças e faça a diferença.")

    st.markdown(f"💡 **Dica final:** Foque em {random.choice(['reciclagem', 'economia de água', 'redução de plásticos'])} para impactar mais o planeta.")

    if st.button("🔁 Reiniciar Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# =======================
# FLUXO PRINCIPAL
# =======================
if "quiz_iniciado" not in st.session_state:
    tela_inicio()
else:
    fase = st.session_state.get("fase", "perguntas")

    if fase == "resultado":
        exibir_resultado()
    else:
        exibir_pergunta()
