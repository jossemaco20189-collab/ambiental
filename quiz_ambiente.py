import streamlit as st
import time  # Para o cronômetro simples
import random  # Para fun facts aleatórios

# 🎨 Configurações da página
st.set_page_config(page_title="Quiz Ambiental Interativo 🌿", page_icon="🌎", layout="wide")  # Layout wide para apresentações

# 🌿 Estilo personalizado (CSS com mais animações e elementos criativos)
st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, #dfffe2, #a8e6cf) fixed;
            background-size: cover; /* Adicionado para fundo responsivo */
            font-family: 'Segoe UI', sans-serif;
            animation: fadeIn 1s ease-in, particles 50s linear infinite; /* Animação de partículas sutis */
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes particles {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }
        .main {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0px 0px 20px rgba(0, 100, 0, 0.3);
            animation: slideIn 0.8s ease-out;
        }
        @keyframes slideIn {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        h1, h2 {
            text-align: center;
            color: #2b7a0b;
            text-shadow: 1px 1px 2px #a8e6cf;
        }
        .question-card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            transition: 0.3s;
            border-left: 6px solid #4CAF50;
            animation: fadeInUp 0.5s ease;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .question-card:hover {
            transform: scale(1.03);
            background-color: #eaffea;
        }
        .stSlider:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
            margin-bottom: 20px;
            animation: fadeIn 0.5s ease;
        }
        .progress-bar-fill {
            height: 25px;
            background: linear-gradient(90deg, #4CAF50, #2e8b57);
            width: 0;
            transition: width 0.5s ease-in-out;
        }
        /* Estilo para confetes no final (simples animação CSS) */
        .confetti {
            position: absolute;
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
    </style>
""", unsafe_allow_html=True)

# Lista de fun facts ambientais (ideia criativa para engajamento)
fun_facts = [
    "Sabia que reciclar uma lata de alumínio economiza energia suficiente para ouvir rádio por 3 horas?",
    "Plantar árvores ajuda a combater o aquecimento global – cada árvore absorve CO2!",
    "Reduzir o desperdício de comida pode salvar recursos hídricos equivalentes a 50 piscinas olímpicas por dia."
]

# Função para exibir tela de início (nova ideia para apresentações)
def tela_inicio():
    st.header("Bem-vindo ao Quiz Ambiental Interativo! 🌍")
    st.markdown("Prepare-se para um desafio divertido sobre meio ambiente e biodiversidade. Responda as perguntas e veja como suas atitudes impactam o planeta!")
    st.markdown("**Instruções:**")
    st.markdown("- Responda de 1 (discordo totalmente) a 5 (concordo totalmente).")
    st.markdown("- Há um cronômetro opcional para cada pergunta para tornar mais empolgante.")
    st.markdown("- Clique em 'Iniciar Quiz' para começar!")
    if st.button("Iniciar Quiz 🌱"):
        st.session_state['quiz_iniciado'] = True

# Função para exibir perguntas com cronômetro e fun facts
def exibir_perguntas():
    st.subheader("🌿 Responda as perguntas abaixo:")
    st.markdown("1️⃣ Discordo totalmente ... 5️⃣ Concordo totalmente")
    
    perguntas = [
        "Evito jogar lixo em locais inadequados.",
        "Separo materiais recicláveis em casa.",
        "Procuro reduzir o uso de plástico descartável.",
        "Economizo água nas tarefas do dia a dia.",
        "Desligo luzes e aparelhos que não estão sendo usados.",  # Perguntas originais
        "Participo ou apoio ações de preservação ambiental.",
        "Levo em conta o impacto ambiental ao comprar produtos.",
        "Acredito que atitudes individuais ajudam o planeta.",
        "Procuro aprender mais sobre meio ambiente e biodiversidade.",
        "Acho importante cobrar políticas públicas ambientais.",
        "Uso transporte público ou bicicleta para reduzir emissões.",  # Novas perguntas
        "Planto árvores ou cuido de plantas em casa.",
        "Evito o desperdício de alimentos no meu dia a dia."
    ]
    
    respostas = []
    total_perguntas = len(perguntas)
    st.markdown('<div class="progress-bar"><div class="progress-bar-fill" id="progress-fill" style="width: 0%;"></div></div>', unsafe_allow_html=True)
    
    for i, pergunta in enumerate(perguntas, start=1):
        with st.container():
            st.markdown(f"<div class='question-card'><b>{i}. {pergunta}</b></div>", unsafe_allow_html=True)
            st.write(f"Fun Fact: {random.choice(fun_facts)}")  # Ideia criativa: Fun fact aleatório
            start_time = time.time()  # Inicia cronômetro
            resposta = st.slider("", 1, 5, 3, key=f"pergunta_{i}")
            end_time = time.time()
            tempo_gasto = round(end_time - start_time, 1)  # Tempo em segundos
            st.write(f"Tempo gasto: {tempo_gasto} segundos")  # Feedback interativo
            respostas.append(resposta)
            progresso_pct = (i / total_perguntas) * 100
            st.markdown(f"""
                <script>
                    document.getElementById('progress-fill').style.width = '{progresso_pct}%';
                </script>
            """, unsafe_allow_html=True)
    return respostas

# Função para exibir resultado com efeitos criativos
def exibir_resultado(respostas):
    total = sum(respostas)
    max_pontos = len(respostas) * 5
    proporcao = total / max_pontos
    st.subheader("📊 Seu Resultado Final 📊")
    st.markdown(f"<h3>**Pontuação total:** {total} de {max_pontos}</h3>", unsafe_allow_html=True)
    
    if proporcao >= 0.85:
        st.success("🌎 Excelente! Ganhe um badge: 🏆 Campeão Ambiental!")
        st.markdown('<div class="confetti"></div>', unsafe_allow_html=True)  # Animação de confete
    elif proporcao >= 0.6:
        st.info("🍃 Muito bom! Tente melhorar para o próximo nível.")
    else:
        st.warning("🌱 Hora de agir! Aqui vão dicas personalizadas.")
    
    st.markdown(f"**Dica final:** Baseado na sua pontuação, foque em {random.choice(['reciclagem', 'economia de água', 'redução de plásticos'])} para impactar mais.")

# Fluxo principal
def main():
    if 'quiz_iniciado' not in st.session_state:
        st.session_state['quiz_iniciado'] = False
    if not st.session_state['quiz_iniciado']:
        tela_inicio()
    else:
        respostas = exibir_perguntas()
        if st.button("Ver Resultado Final 🌱"):
            exibir_resultado(respostas)
            if st.button("Reiniciar Quiz"):
                st.session_state['quiz_iniciado'] = False  # Reinicia para apresentações

if __name__ == "__main__":
    main()
