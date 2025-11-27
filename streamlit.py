import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# =========================
# Configuración inicial
# =========================
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

# =========================
# Tema pastel fijo
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #fce4ec 100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Menú lateral (configuración)
# =========================
st.sidebar.title("Configuración del modelo")

# -------- PERSONALIDAD CON SLIDER --------

opciones = [
    "Muy técnica",
    "Técnica",
    "Equilibrada",
    "Creativa",
    "Muy creativa"
]

# Slider solo muestra texto, no números
indice_personalidad = st.sidebar.slider(
    "Estilo de respuesta",
    min_value=0,
    max_value=len(opciones)-1,
    value=2,  # Equilibrada
    step=1,
    format="%d"  # no importa el número, lo ocultamos abajo
)

estilo_respuesta = opciones[indice_personalidad]

# Mapeo estilo → temperatura real
mapa_temperatura = {
    "Muy técnica": 0.1,
    "Técnica": 0.3,
    "Equilibrada": 0.5,
    "Creativa": 0.7,
    "Muy creativa": 0.9
}

temperatura = mapa_temperatura[estilo_respuesta]

# Mostrar info bonita
st.sidebar.markdown(f"🧠 **Estilo actual:** {estilo_respuesta}")
st.sidebar.caption(f"Temperatura real: {temperatura}")

# -------- SELECTOR DE MODELO --------
modelo_seleccionado = st.sidebar.selectbox(
    "Modelo",
    ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
)

# -------- LIMPIAR CONVERSACIÓN --------
if st.sidebar.button("Limpiar conversación"):
    st.session_state.mensajes = []

# =========================
# Crear modelo de chat con la config elegida
# =========================
chat_model = ChatGoogleGenerativeAI(
    model=modelo_seleccionado,
    temperature=temperatura,
)

# =========================
# Historial de mensajes
# =========================
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# =========================
# Input del usuario
# =========================
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)
    st.session_state.mensajes.append(respuesta)
