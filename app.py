import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 1. Configuración de la API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def identificar(img):
    try:
        # USAMOS EL MODELO QUE APARECE EN TU CAPTURA DE PANTALLA
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = (
            "Eres un botánico experto de la Península de Yucatán. "
            "Identifica esta planta: nombre científico, común y descripción breve."
        )
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Aviso del sistema: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")
st.write("Identificación botánica con Gemini 3 Flash")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("Subir imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner("Analizando con Gemini 3..."):
            resultado = identificar(img)
            st.success(resultado)
