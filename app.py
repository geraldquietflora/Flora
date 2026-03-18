import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def identificar(img):
    try:
        # FORZAMOS EL MODELO DE ALTA CUOTA (1,500 al día)
        # Usamos el nombre base sin el sufijo 'preview'
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("🔬 Usando: `Gemini 1.5 Flash` (Cuota alta)")
        
        prompt = (
            "Eres un botánico experto de la Península de Yucatán. "
            "Identifica esta planta: nombre científico, común y descripción breve."
        )
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        # Si el 1.5 da error 404, el sistema nos lo dirá aquí
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
        with st.spinner("Consultando herbario digital..."):
            resultado = identificar(img)
            st.success(resultado)
