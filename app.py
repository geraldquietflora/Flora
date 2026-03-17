import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 1. Configuración de seguridad
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ La llave no se encuentra en los Secrets de Streamlit.")
    st.stop()

# 2. Inicialización limpia
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usamos la versión flash que es la más rápida y gratuita
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al configurar Google AI: {e}")

def identificar(img):
    try:
        # Prompt directo y científico
        prompt = "Identifica esta planta de la Península de Yucatán. Dame Nombre científico, Nombre común y una descripción breve."
        # Enviamos la imagen directamente
        response = model.generate_content([prompt, img])
        
        if response.text:
            return response.text
        else:
            return "El servidor respondió pero no generó texto. Intenta con otra foto."
    except Exception as e:
        # Este mensaje nos dirá si la llave sigue bloqueada o si el modelo no existe
        return f"Aviso del sistema: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")
st.write("Herramienta de identificación botánica regional.")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("Subir imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    
    if st.button("🔍 ANALIZAR ESPECIE"):
        with st.spinner("Procesando morfología..."):
            resultado = identificar(img)
            st.markdown("### Resultado:")
            st.info(resultado)
