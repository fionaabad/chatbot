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
# Tema pastel + burbujas de colores
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #fce4ec 100%);
    }
    .user_msg {
        background-color: #bbdefb;
        border-radius: 15px;
        padding: 10px;
    }
    .ai_msg {
        background-color: #f8bbd0;
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Menú lateral (configuración)
# =========================
st.sidebar.title("Configuración del modelo")

# -------- Estilo / temperatura con slider --------
opciones_estilo = [
    "Muy técnica",
    "Técnica",
    "Equilibrada",
    "Creativa",
    "Muy creativa"
]

indice_personalidad = st.sidebar.slider(
    "Estilo de respuesta",
    min_value=0,
    max_value=len(opciones_estilo) - 1,
    value=2,  # Equilibrada por defecto
    step=1,
)

estilo_respuesta = opciones_estilo[indice_personalidad]

mapa_temperatura = {
    "Muy técnica": 0.1,
    "Técnica": 0.3,
    "Equilibrada": 0.5,
    "Creativa": 0.7,
    "Muy creativa": 0.9,
}

temperatura = mapa_temperatura[estilo_respuesta]

st.sidebar.markdown(f"🧠 **Estilo actual:** {estilo_respuesta}")
st.sidebar.caption(f"Temperatura real: {temperatura}")

# -------- Selector de modelo --------
modelo_seleccionado = st.sidebar.selectbox(
    "Modelo",
    ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
)

# -------- Modo explicación paso a paso --------
modo_explicativo = st.sidebar.checkbox("Modo explicación paso a paso")

# -------- Personalidad del asistente --------
personalidad = st.sidebar.selectbox(
    "Personalidad",
    ["Normal", "Profesor paciente", "Comediante", "Experto formal", "Explica como si tuviera 5 años"],
)

# -------- Botón para limpiar conversación --------
if st.sidebar.button("Limpiar conversación"):
    st.session_state.mensajes = []

# Mostrar info arriba
st.caption(f"**Modelo activo:** {modelo_seleccionado} · **Estilo:** {estilo_respuesta} · **Personalidad:** {personalidad}")

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

# Mostrar historial ya guardado con burbujas de colores
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    css_class = "ai_msg" if role == "assistant" else "user_msg"
    with st.chat_message(role):
        st.markdown(f"<div class='{css_class}'>{msg.content}</div>", unsafe_allow_html=True)

# =========================
# Input del usuario
# =========================
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Construir prefijo según personalidad y modo explicativo
    prefijo = ""

    if personalidad == "Profesor paciente":
        prefijo += "Responde de manera clara y pedagógica, como un profesor paciente. "
    elif personalidad == "Comediante":
        prefijo += "Responde con humor y chistes, pero sin dejar de ser útil. "
    elif personalidad == "Experto formal":
        prefijo += "Responde de manera muy formal y profesional. "
    elif personalidad == "Explica como si tuviera 5 años":
        prefijo += "Explícalo con palabras muy sencillas, como a una niña de 5 años. "

    if modo_explicativo:
        prefijo += "Explica paso a paso y con mucho detalle. "

    contenido_para_modelo = prefijo + pregunta

    # Mostrar y guardar mensaje del usuario (solo el texto original, sin prefijos)
    with st.chat_message("user"):
        st.markdown(f"<div class='user_msg'>{pregunta}</div>", unsafe_allow_html=True)
    st.session_state.mensajes.append(HumanMessage(content=contenido_para_modelo))

    # Llamar al modelo con todo el historial
    respuesta = chat_model.invoke(st.session_state.mensajes)

    # Mostrar y guardar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(f"<div class='ai_msg'>{respuesta.content}</div>", unsafe_allow_html=True)
    st.session_state.mensajes.append(respuesta)
