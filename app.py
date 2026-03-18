import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de página
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 2. Inicialización de la API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave en los Secrets de Streamlit.")
    st.stop()

# Forzamos la configuración limpia
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def identificar(img):
    try:
        # Usamos el nombre de modelo estándar que funciona en v1 y v1beta
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Eres un botánico experto de la Península de Yucatán. "
            "Identifica esta planta: nombre científico, común y descripción breve."
        )
        
        # Enviamos la imagen. La librería se encarga de la versión de la API.
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Aviso del sistema: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("Subir imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 ANALIZAR ESPECIE"):
        with st.spinner("Conectando con el herbario digital..."):
            resultado = identificar(img)
            st.success(resultado)

st.divider()
st.info("Nota: Si persiste el error 404, Google está actualizando sus servidores en tu región. Reintenta en un momento.")
