import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# Conexión con tu API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def identificar_especie(img):
    try:
        # Ahora usamos el 1.5 Flash sin miedo al límite
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Eres un botánico experto en la Península de Yucatán. Identifica esta planta: "
            "1. Nombre científico (cursivas). 2. Nombre común regional. "
            "3. Familia. 4. Nota breve de su ecología local."
        )
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Aviso del sistema: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA (Modo Profesional)")
st.caption("Uso de alta capacidad habilitado para investigación.")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("Subir imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 ANALIZAR AHORA"):
        with st.spinner("Procesando con capacidad ilimitada..."):
            resultado = identificar_especie(img)
            st.success(resultado)
