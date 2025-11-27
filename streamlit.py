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

# Selector de "personalidad" en vez de temperatura numérica
estilo_respuesta = st.sidebar.radio(
    "Estilo de respuesta",
    ["Muy técnica", "Equilibrada", "Creativa"],
)

# Mapeo de estilo -> temperatura
if estilo_respuesta == "Muy técnica":
    temperatura = 0.1
elif estilo_respuesta == "Equilibrada":
    temperatura = 0.5
else:  # "Creativa"
    temperatura = 0.9

# Opcional: mostrar la temperatura real como info
st.sidebar.caption(f"Temperatura real: {temperatura}")

# Select para elegir el modelo
modelo_seleccionado = st.sidebar.selectbox(
    "Modelo",
    ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
)

# Botón para limpiar la conversación
if st.sidebar.button("Limpiar conversación"):
    st.session_state.mensajes = []

# =========================
# Crear el modelo de chat con la config elegida
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

# Mostrar historial ya guardado
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# =========================
# Input del usuario
# =========================
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar y guardar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    # Llamar al modelo con todo el historial
    respuesta = chat_model.invoke(st.session_state.mensajes)

    # Mostrar y guardar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)
    st.session_state.mensajes.append(respuesta)
