import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

if "GOOGLE_API_KEY" in st.secrets:
    # Esta configuración es la estándar para Google Cloud
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura la nueva API Key en Secrets.")
    st.stop()

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 ANALIZAR"):
        with st.spinner('Conectando con Google Cloud...'):
            try:
                # El modelo 'gemini-1.5-flash' es el correcto para producción
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                response = model.generate_content([
                    "Identifica esta planta: Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059.", 
                    img
                ])
                
                st.success("Análisis exitoso")
                st.info(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")
