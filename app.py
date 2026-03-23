import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🌿 Flora: Análisis Botánico")

# 1. Conexión directa con el Secret
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Error: No se encontró la API Key en los Secrets.")
    st.stop()

# 2. Interfaz de cámara
archivo = st.camera_input("Capturar planta")

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Analizando...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                prompt = "Identifica esta planta: Nombre científico, familia y nombres en Maya."
                
                response = model.generate_content([prompt, img])
                st.success("¡Logrado!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")
