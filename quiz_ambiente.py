import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Quiz Ambiental 🌱", page_icon="🌿", layout="centered")

# ============================
# DADOS DAS QUESTÕES
# ============================
QUESTOES = [
    {
        "pergunta": "Qual dessas ações ajuda mais o meio ambiente?",
        "opcoes": [
            "Usar copo descartável no trabalho",
            "Andar de carro sozinho todos os dias",
            "Reciclar o lixo e economizar água",
            "Deixar luzes acesas o dia todo"
        ],
        "resposta": 2
    },
    {
        "pergunta": "O que é coleta seletiva?",
        "opcoes": [
            "Separar o lixo por tipo de material",
            "Jogar tudo no mesmo saco de lixo",
            "Deixar o lixo acumular até o final do mês",
            "Evitar jogar o lixo fora"
        ],
        "resposta": 0
    },
    {
        "pergunta": "Qual fonte de energia é renovável?",
        "opcoes": [
            "Petróleo",
            "Carvão mineral",
            "Energia solar",
            "Gás natural"
        ],
        "resposta": 2
    }
]

# ============================
# FUNÇÕES AUXILIARES
# ============================
def salvar_no_ranking(nome, pontuacao):
    """Salva o nome e a pontuação em um arquivo CSV."""
    arquivo = "ranking_quiz.csv"
    dados = pd.DataFrame([[nome, pontuacao]], columns=["Nome", "Pontuação"])
    if os.path.exists(arquivo):
        antigo = pd.read_csv(arquivo)
        dados = pd.concat([antigo, dados], ignore_index=True)
    dados.to_csv(arquivo, index=False)

def carregar_ranking():
    """Lê o ranking salvo."""
    arquivo = "ranking_quiz.csv"
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    return pd.DataFrame(columns=["Nome", "Pontuação"])

def calcular_categoria(total, max_pontos):
    """Classifica o jogador com base na pontuação."""
    proporcao = total / max_pontos
    if proporcao >= 0.85:
        return "Campeão Ambiental", "🏆"
    elif proporcao >= 0.6:
        return "Protetor Verde", "🌿"
    elif proporcao >= 0.4:
        return "Aprendiz Consciente", "🌱"
    else:
        return "Iniciante — Hora de Agir", "🌍"

def exibir_resultado(respostas, nome_usuario):
    """Exibe o resultado final."""
    total = sum(respostas)
    max_p = len(QUESTOES) * 5
    categoria, emoji = calcular_categoria(total, max_p)
    st.header('Resultado')
    st.write(f'{emoji} {categoria} — {total}/{max_p}')
    salvar_no_ranking(nome_usuario or 'Anônimo', total)
    if st.button('Reiniciar Quiz 🔄'):
        st.session_state.clear()
        st.rerun()

# ============================
# INTERFACE DO QUIZ
# ============================
st.title("🌎 Quiz Ambiental Interativo")
st.markdown("### Descubra o quanto você entende sobre sustentabilidade!")

nome = st.text_input("Digite seu nome para começar:")

if st.button("Iniciar quiz 🌱") and nome.strip():
    st.session_state["quiz_iniciado"] = True
    st.session_state["respostas"] = []
    st.rerun()

# Quando o quiz começa
if "quiz_iniciado" in st.session_state:
    respostas = st.session_state["respostas"]
    for i, q in enumerate(QUESTOES):
        st.subheader(f"Pergunta {i + 1}: {q['pergunta']}")
        resposta = st.radio(
            "Escolha uma alternativa:",
            q["opcoes"],
            key=f"pergunta_{i}"
        )
        if st.button(f"Confirmar resposta {i+1}"):
            if q["opcoes"].index(resposta) == q["resposta"]:
                respostas.append(5)
            else:
                respostas.append(0)
            st.session_state["respostas"] = respostas
            st.rerun()

    if len(respostas) == len(QUESTOES):
        exibir_resultado(respostas, nome)

# ============================
# RANKING
# ============================
st.divider()
st.subheader("🏅 Ranking dos Jogadores")
ranking = carregar_ranking()
if not ranking.empty:
    ranking = ranking.sort_values(by="Pontuação", ascending=False)
    st.dataframe(ranking, use_container_width=True)
else:
    st.write("Nenhum resultado registrado ainda.")

# ============================
# RODAPÉ
# ============================
st.markdown("<div style='text-align:center; opacity:0.7;'>Projeto educativo de conscientização ambiental 🌿</div>", unsafe_allow_html=True)
