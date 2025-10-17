import streamlit as st
import time  # Para cronômetro
import random  # Para fun facts aleatórios

# 🎨 Configurações da página
st.set_page_config(page_title="Quiz Ambiental Interativo 🌿", page_icon="🌎", layout="wide")

# 🌿 Estilo personalizado (CSS aprimorado com animações, gradientes e responsividade)
st.markdown("""
    <style>
        /* Estilos gerais: Gradientes temáticos e responsividade */
        body {
            background: linear-gradient(180deg, #dfffe2, #a8e6cf, #2196F3); /* Gradiente de natureza */
            font-family: 'Segoe UI', sans-serif;
            animation: fadeIn 1s ease-in;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .main-container {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0px 0px 20px rgba(0, 100, 0, 0.3);
            animation: slideIn 0.8s ease-out;
            max-width: 800px; /* Responsivo */
            width: 100%;
        }
        @keyframes slideIn {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        h1, h2 {
            text-align: center;
            color: #2b7a0b;
            text-shadow: 1px 1px 2px #a8e6cf;
            animation: pulseText 2s infinite;
        }
        @keyframes pulseText {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        /* Ícone animado do planeta na tela inicial */
        .planet-icon {
            font-size: 50px;
            animation: rotatePlanet 5s linear infinite;
        }
        @keyframes rotatePlanet {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .question-card {
            background: linear-gradient(135deg, #eaffea, #ffffff);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 6px solid #4CAF50;
            animation: fadeInUp 0.5s ease;
            transition: transform 0.3s;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .question-card:hover {
            transform: scale(1.03);
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
            50% { transform: scale(1.02); }
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
            animation: fadeIn 0.5s ease;
        }
        .progress-bar-fill {
            height: 25px;
            background: linear-gradient(90deg, #4CAF50, #2e8b57);
            width: 0;
            transition: width 0.5s ease-in-out;
            animation: progressAnim 1s ease-in-out;
        }
        @keyframes progressAnim {
            from { width: 0; }
            to { width: var(--progress-width); }
        }
        
        /* Confetes para tela final */
        .confetti {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            opacity: 0;
            animation: confettiFall 5s linear forwards;
        }
        @keyframes confettiFall {
            from { opacity: 1; }
            to { opacity: 0; transform: translateY(100vh); }
        }
        
        /* Responsividade */
        @media (max-width: 600px) {
            .main-container { padding: 20px; }
            h1 { font-size: 24px; }
        }
    </style>
""", unsafe_allow_html=True)

# Lista de fun facts e dicas educativas
fun_facts = [
    "Sabia que reciclar uma lata de alumínio economiza energia para ouvir rádio por 3 horas?",
    "Plantar árvores absorve CO2 e combate o aquecimento global!",
    "Reduzir desperdício de comida economiza água equivalente a 50 piscinas olímpicas por dia."
]
dicas = [
    "Dica: Sempre separe o lixo reciclável para preservar o meio ambiente.",
    "Curiosidade: Usar bicicleta reduz emissões de CO2 e melhora sua saúde."
]

# Função para UI: Exibe elementos com animações
def ui_exibir_elemento(placeholder, content, animation_class):
    with placeholder:
        st.markdown(f'<div class="{animation_class}">{content}</div>', unsafe_allow_html=True)

# Lógica do quiz: Calcula pontuação e gamificação
def quiz_logic_perguntas(dificuldade):
    perguntas = [
        "Evito jogar lixo em locais inadequados.",
        "Separo materiais recicláveis em casa.",
        # ... (outras perguntas originais)
    ]
    if dificuldade == "fácil":
        return perguntas[:5]  # Menos perguntas
    elif dificuldade == "médio":
        return perguntas[:8]
    else:  # Difícil
        return perguntas  # Todas
    
def quiz_logic_calcular_pontuacao(respostas, dificuldade):
    total = sum(respostas)
    multiplicador = {"fácil": 1, "médio": 1.2, "difícil": 1.5}[dificuldade]
    return int(total * multiplicador)

# Tela inicial com gamificação e avatar
def tela_inicio():
    st.title("Quiz Ambiental Interativo 🌎")
    st.markdown('<div class="planet-icon">🌎</div>', unsafe_allow_html=True)
    st.markdown("Prepare-se para um desafio divertido! 🌳 Seu guia: Um protetor da floresta.")
    dificuldade = st.selectbox("Escolha o nível:", ["fácil", "médio", "difícil"])
    if st.button("Iniciar Quiz 🌱"):
        st.session_state['quiz_iniciado'] = True
        st.session_state['dificuldade'] = dificuldade
        st.session_state['respostas'] = []

# Exibir perguntas com feedback e modo educativo
def exibir_perguntas():
    perguntas = quiz_logic_perguntas(st.session_state['dificuldade'])
    respostas = st.session_state['respostas']
    total_perguntas = len(perguntas)
    
    for i, pergunta in enumerate(perguntas, start=1):
        placeholder = st.empty()  # Para transições suaves
        ui_exibir_elemento(placeholder, f"<div class='question-card'>{i}. {pergunta}</div>", "slideIn")
        st.write(f"Fun Fact: {random.choice(fun_facts)}")
        st.write(f"Dica: {random.choice(dicas)}")
        
        resposta = st.slider("", 1, 5, 3, key=f"pergunta_{i}")
        respostas.append(resposta)
        
        # Feedback animado
        feedback = "✅" if resposta >= 3 else "❌"
        st.markdown(f'<div style="font-size: 24px; animation: fadeIn 0.5s;">{feedback} {random.choice(["🌱", "🌎"])}</div>', unsafe_allow_html=True)
        
        # Som de feedback (embutido)
        if resposta >= 3:
            st.markdown('<audio autoplay><source src="https://freesound.org/data/previews/171/171104_2341904-lq.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)  # Som de folhas
        else:
            st.markdown('<audio autoplay><source src="https://freesound.org/data/previews/80/80973_427718-lq.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)  # Som de água
        
        st.session_state['respostas'] = respostas  # Atualiza sessão
        progresso_pct = (i / total_perguntas) * 100
        st.markdown(f'<div class="progress-bar"><div class="progress-bar-fill" style="--progress-width: {progresso_pct}%; width: {progresso_pct}%;"></div></div>', unsafe_allow_html=True)

# Exibir resultado com efeitos finais
def exibir_resultado():
    respostas = st.session_state['respostas']
    pontuacao = quiz_logic_calcular_pontuacao(respostas, st.session_state['dificuldade'])
    max_pontos = len(respostas) * 5
    proporcao = pontuacao / max_pontos
    
    st.subheader("📊 Seu Resultado Final 📊")
    st.markdown(f"<h3>Pontuação: {pontuacao} de {max_pontos}</h3>", unsafe_allow_html=True)
    
    if proporcao >= 0.85:
        ranking = "Campeão Ambiental 🏆"
        st.markdown('<div class="confetti"></div>', unsafe_allow_html=True)  # Confetes
        st.success(f"🌎 Excelente! Você é um {ranking}!")
    elif proporcao >= 0.6:
        ranking = "Protetor da Floresta 🌳"
        st.info(f"🍃 Muito bom! Você é um {ranking}.")
    else:
        ranking = "Iniciante Ecológico 🌱"
        st.warning(f"🌱 Hora de agir! Você é um {ranking}.")
    
    st.markdown(f"Insights: Foque em {random.choice(['reciclagem', 'economia de água'])} para melhorar.")
    
    # Música de encerramento (ambiente)
    st.markdown('<audio autoplay loop><source src="https://freesound.org/data/previews/339/339802_542669-lq.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
    
    if st.button("Reiniciar Quiz"):
        st.experimental_rerun()  # Efeito suave de reinício

# Fluxo principal
def main():
    if 'quiz_iniciado' not in st.session_state:
        st.session_state['quiz_iniciado'] = False
    if not st.session_state['quiz_iniciado']:
        tela_inicio()
    else:
        exibir_perguntas()
        if st.button("Ver Resultado"):
            exibir_resultado()

if __name__ == "__main__":
    main()
