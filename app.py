import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered")

# Configuración con la librería estable (evita el error v1beta)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Error: Revisa los Secrets en Streamlit Cloud.")
    st.stop()

st.title("🌿 Flora: Análisis Botánico")

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Analizando...'):
            try:
                # Nombre de modelo estándar (sin prefijos models/ ni v1beta)
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = "Identifica esta planta: Nombre científico, familia, nombres comunes (incluye Maya), hábitat y estatus NOM-059."
                response = model.generate_content([prompt, img])
                
                st.success("Resultado:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error de comunicación: {e}")
