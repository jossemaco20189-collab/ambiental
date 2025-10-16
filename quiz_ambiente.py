import streamlit as st

# 🎨 Configurações da página
st.set_page_config(page_title="Quiz Ambiental Interativo 🌿", page_icon="🌎", layout="centered")

# 🌿 Estilo personalizado (CSS responsivo e simplificado)
st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, #dfffe2, #a8e6cf) fixed;
            font-family: 'Segoe UI', sans-serif;
            animation: fadeIn 1s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .main {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0px 0px 10px rgba(0, 100, 0, 0.1);
            animation: slideIn 0.6s ease-out;
        }
        @keyframes slideIn {
            from { transform: translateY(10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        h1, h2, h3 {
            text-align: center;
            color: #2b7a0b;
            font-size: 20px;  /* Fonte base maior para visibilidade */
        }
        .question-container {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #4CAF50;  /* Borda mais simples */
            animation: fadeInUp 0.5s ease;
            overflow: auto;  /* Evita sobreposição */
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stSlider {
            width: 100%;
            margin: 20px 0;  /* Mais espaço ao redor */
            font-size: 16px;  /* Fonte maior para mobile */
        }
        .stButton>button {
            background: linear-gradient(90deg, #4CAF50, #2e8b57);
            color: white;
            font-size: 16px;
            padding: 10px 15px;
            border-radius: 10px;
            border: none;
            transition: 0.3s;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        .stButton>button:hover {
            transform: scale(1.05);
        }
        /* Media queries aprimoradas para mobile */
        @media (max-width: 600px) {
            .main {
                padding: 10px;
                border-radius: 5px;
            }
            h1, h2, h3 {
                font-size: 16px;
            }
            .question-container {
                padding: 10px;
                font-size: 14px;
                margin: 10px 0;
            }
            .stSlider {
                font-size: 14px;
                margin: 10px 0;
            }
            .stButton>button {
                font-size: 14px;
                padding: 8px 12px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Lista de perguntas e fun facts
perguntas = [
    "Você evita jogar lixo em locais inadequados?",
    "Você separa materiais recicláveis em casa?",
    "Você procura reduzir o uso de plástico descartável?",
    "Você economiza água nas tarefas do dia a dia?",
    "Você desliga luzes e aparelhos que não estão sendo usados?",
    "Você participa ou apoia ações de preservação ambiental?",
    "Você leva em conta o impacto ambiental ao comprar produtos?",
    "Você acredita que atitudes individuais ajudam o planeta?",
    "Você procura aprender mais sobre meio ambiente e biodiversidade?",
    "Você acha importante cobrar políticas públicas ambientais?"
]

fun_facts = [
    "Evitar lixo ajuda a preservar rios e oceanos.",
    "Reciclagem reduz o desperdício e economiza recursos naturais.",
    "Reduzir plástico protege animais marinhos da poluição.",
    "Economizar água preserva ecossistemas aquáticos.",
    "Desligar aparelhos diminui a emissão de gases de efeito estufa.",
    "Ações de preservação ajudam a manter a biodiversidade.",
    "Compras conscientes reduzem o impacto no clima global.",
    "Atitudes individuais podem inspirar mudanças coletivas.",
    "Aprender sobre o meio ambiente promove a sustentabilidade.",
    "Políticas ambientais protegem florestas e espécies em risco."
]

# Função para tela de início
def tela_inicio():
    st.header("Bem-vindo ao Quiz Ambiental Interativo! 🌍")
    st.markdown("Responda 'Sim', 'Às vezes' ou 'Não' para cada pergunta.")
    if st.button("Iniciar Quiz 🌱"):
        st.session_state['quiz_iniciado'] = True
        st.session_state['pergunta_atual'] = 0
        st.session_state['respostas'] = []

# Função para exibir uma pergunta por vez
def exibir_pergunta():
    if 'pergunta_atual' in st.session_state and st.session_state['pergunta_atual'] < len(perguntas):
        idx = st.session_state['pergunta_atual']
        pergunta = perguntas[idx]
        fun_fact = fun_facts[idx]
        
        st.markdown(f"<div class='question-container'><h3>{pergunta}</h3><p><i>{fun_fact}</i></p></div>", unsafe_allow_html=True)
        
        resposta = st.slider("Responda: 1 - Não, 2 - Às vezes, 3 - Sim", 1, 3, 2, key=f"slider_{idx}")
        
        if st.button("Próxima pergunta"):
            st.session_state['respostas'].append(resposta)
            st.session_state['pergunta_atual'] += 1
    else:
        exibir_resultado(st.session_state['respostas'])

# Função para exibir resultado
def exibir_resultado(respostas):
    total = sum(respostas)
    max_pontos = len(respostas) * 3
    proporcao = total / max_pontos if max_pontos > 0 else 0
    
    st.subheader("📊 Seu Resultado Final 📊")
    st.markdown(f"**Pontuação total:** {total} de {max_pontos}")
    
    if proporcao >= 0.8:
        st.success("🌎 Excelente! Você é um campeão ambiental!")
    elif proporcao >= 0.5:
        st.info("🍃 Bom trabalho! Há espaço para melhorias.")
    else:
        st.warning("🌱 Vamos começar a mudar hábitos juntos.")

# Fluxo principal
def main():
    if 'quiz_iniciado' not in st.session_state:
        st.session_state['quiz_iniciado'] = False
    if not st.session_state['quiz_iniciado']:
        tela_inicio()
    else:
        exibir_pergunta()
        if st.button("Reiniciar Quiz"):
            st.session_state['quiz_iniciado'] = False

if __name__ == "__main__":
    main()

