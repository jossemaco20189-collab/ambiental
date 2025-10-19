import streamlit as st
import random
import time

# --- Configurações da página ---
st.set_page_config(
    page_title="Quiz Ambiental 🌿",
    page_icon="🌎",
    layout="centered"
)

# --- CSS customizado para deixar o visual elegante ---
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #e6f4ea 0%, #ffffff 100%);
    color: #1b4332;
    font-family: "Poppins", sans-serif;
}
h1, h2, h3 {
    text-align: center;
    color: #2d6a4f;
}
.stButton button {
    background: linear-gradient(90deg, #40916c, #2d6a4f);
    color: white;
    border-radius: 12px;
    font-weight: bold;
    transition: 0.3s;
}
.stButton button:hover {
    background: linear-gradient(90deg, #2d6a4f, #1b4332);
    transform: scale(1.03);
}
.slider {
    accent-color: #2d6a4f;
}
hr {
    border: none;
    border-top: 2px solid #74c69d;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Título principal ---
st.title("🌎 Quiz Ambiental Interativo 🌿")
st.markdown("### Descubra seu perfil ecológico de um jeito divertido!")

st.markdown("""
### 🌿 Como jogar
Avalie o quanto você **coloca em prática** cada atitude ambiental no seu dia a dia.  
Use a escala abaixo:

- **1️⃣ Nunca faço isso**  
- **2️⃣ Raramente**  
- **3️⃣ Às vezes**  
- **4️⃣ Frequentemente**  
- **5️⃣ Sempre**

✨ *Não existe certo ou errado — o objetivo é refletir sobre suas ações e descobrir seu perfil ecológico!*
""")

# --- Lista de perguntas ---
perguntas = [
    "Evito jogar lixo em locais inadequados.",
    "Procuro economizar água durante o banho ou ao escovar os dentes.",
    "Desligo luzes e aparelhos que não estou usando.",
    "Reaproveito ou reciclo materiais sempre que possível.",
    "Participo ou apoio projetos de proteção ambiental.",
    "Evito o uso excessivo de plástico descartável.",
    "Procuro usar transporte coletivo, bicicleta ou andar a pé sempre que posso.",
    "Cuido de plantas ou árvores ao meu redor.",
    "Incentivo outras pessoas a terem atitudes sustentáveis.",
    "Procuro me informar sobre temas ligados ao meio ambiente."
]

# --- Variável de pontuação total ---
pontuacao_total = 0

# --- Exibe cada pergunta ---
for i, pergunta in enumerate(perguntas):
    st.markdown(f"#### {i+1}. {pergunta}")
    
    resposta = st.slider(
        "Com que frequência você pratica essa ação?",
        1, 5, 3,
        format="%d",
        help="1 = Nunca faço isso · 2 = Raramente · 3 = Às vezes · 4 = Frequentemente · 5 = Sempre",
        key=f"slider_{i}"
    )
    pontuacao_total += resposta
    st.markdown("<hr>", unsafe_allow_html=True)

# --- Botão de resultado ---
if st.button("Ver resultado 🌱"):
    media = pontuacao_total / len(perguntas)

    # Determina mensagem de acordo com pontuação
    if media < 2:
        resultado = "🌪️ Você ainda pode melhorar seus hábitos ambientais."
        cor = "#ff6b6b"
    elif media < 3.5:
        resultado = "🌾 Você está no caminho certo! Continue evoluindo."
        cor = "#ffd166"
    elif media < 4.5:
        resultado = "🌿 Excelente! Suas ações já fazem diferença!"
        cor = "#74c69d"
    else:
        resultado = "🌎 Incrível! Você é um verdadeiro guardião da Terra!"
        cor = "#1b4332"

    st.markdown(f"""
    <div style='text-align:center; padding:25px; background:{cor}20; border-radius:15px;'>
        <h2 style='color:{cor};'>{resultado}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Pequena animação de feedback
    with st.spinner("Calculando seu impacto ambiental... 🌍"):
        time.sleep(2)
    st.balloons()

# --- Rodapé ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#52796f; font-size:14px;'>
Feito com 💚 por [Seu Nome ou Equipe Ambiental]
</div>
""", unsafe_allow_html=True)
