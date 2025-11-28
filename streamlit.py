import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# =========================
# Configuración inicial
# =========================
st.set_page_config(page_title="Chatbot Pastel", page_icon="💖")

# =========================
# ESTILOS ESTÉTICOS (pastel + animaciones + botones + input + sidebar)
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #e3f2fd 0%, #fce4ec 100%);
}

/* Sidebar degradado */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fce4ec, #e3f2fd);
}

/* Burbujas usuario */
.user_msg {
    background-color: #bbdefb !important;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 2px 8px #00000020;
    animation: fadeIn 0.4s ease-in-out;
}

/* Burbujas asistente */
.ai_msg {
    background-color: #f8bbd0 !important;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 2px 8px #00000020;
    animation: fadeIn 0.4s ease-in-out;
}

/* Animación suave */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Input del chat redondeado */
div[data-testid="stChatInput"] textarea {
    border-radius: 12px !important;
    padding: 12px !important;
    background-color: #ffffffdd !important;
}

/* Botones pastel */
button[kind="primary"] {
    background-color: #90caf9 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
}

button[kind="secondary"] {
    background-color: #f8bbd0 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
}

/* Cabecera bonita */
.header_box {
    padding: 18px;
    border-radius: 15px;
    background: linear-gradient(90deg, #bbdefb, #f8bbd0);
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #333;
    box-shadow: 0 2px 8px #00000020;
}

</style>
""", unsafe_allow_html=True)


# =========================
# Cabecera
# =========================
st.markdown("<div class='header_box'>✨ Bienvenida a tu Chatbot Pastel ✨</div>", unsafe_allow_html=True)
st.write("")


# =========================
# Menú lateral — Configuración
# =========================
st.sidebar.title("⚙️ Configuración del modelo")

# Estilo de respuesta (temperatura)
opciones_estilo = [
    "Muy técnica",
    "Técnica",
    "Equilibrada",
    "Creativa",
    "Muy creativa"
]

indice_personalidad = st.sidebar.slider(
    "🎨 Estilo de respuesta",
    min_value=0,
    max_value=len(opciones_estilo) - 1,
    value=2,
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

st.sidebar.markdown(f"🧠 **Estilo:** {estilo_respuesta}")
st.sidebar.caption(f"Temperatura real: {temperatura}")

# Selector de modelo
modelo_seleccionado = st.sidebar.selectbox(
    "🤖 Modelo",
    ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
)

# Modo explicación paso a paso
modo_explicativo = st.sidebar.checkbox("📘 Modo explicación paso a paso")

# Personalidad
personalidad = st.sidebar.selectbox(
    "🎭 Personalidad del asistente",
    ["Normal", "Profesor paciente", "Comediante", "Experto formal", "Explica como si tuviera 5 años"],
)

# Botón limpiar
if st.sidebar.button("🧹 Limpiar conversación"):
    st.session_state.mensajes = []

# Mostrar info arriba
st.caption(f"**Modelo activo:** {modelo_seleccionado} · **Estilo:** {estilo_respuesta} · **Personalidad:** {personalidad}")


# =========================
# Crear modelo
# =========================
chat_model = ChatGoogleGenerativeAI(
    model=modelo_seleccionado,
    temperature=temperatura,
)


# =========================
# Historial
# =========================
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    css_class = "ai_msg" if role == "assistant" else "user_msg"

    with st.chat_message(role):
        st.markdown(f"<div class='{css_class}'>{msg.content}</div>", unsafe_allow_html=True)


# =========================
# Input del usuario
# =========================
pregunta = st.chat_input("Escribe tu mensaje ✨")

if pregunta:
    # Prefijos de personalidad
    prefijo = ""

    if personalidad == "Profesor paciente":
        prefijo += "Responde de manera clara y pedagógica, como un profesor paciente. "
    elif personalidad == "Comediante":
        prefijo += "Responde con humor y chistes sin perder utilidad. "
    elif personalidad == "Experto formal":
        prefijo += "Responde con tono serio y profesional. "
    elif personalidad == "Explica como si tuviera 5 años":
        prefijo += "Explícalo con palabras muy simples, como a una niña de 5 años. "

    if modo_explicativo:
        prefijo += "Explica paso a paso y con mucho detalle. "

    contenido_para_modelo = prefijo + pregunta

    # Mostrar mensaje usuario
    with st.chat_message("user"):
        st.markdown(f"<div class='user_msg'>{pregunta}</div>", unsafe_allow_html=True)

    # Guardar
    st.session_state.mensajes.append(HumanMessage(content=contenido_para_modelo))

    # Respuesta IA
    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(f"<div class='ai_msg'>{respuesta.content}</div>", unsafe_allow_html=True)

    st.session_state.mensajes.append(respuesta)
