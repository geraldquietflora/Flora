import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# Configuración de API desde Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 ANALIZAR"):
        with st.spinner('Procesando...'):
            try:
                # El modelo estándar que siempre ha funcionado
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)

                prompt = "Identifica esta planta: Nombre científico, familia, nombres comunes (incluye Maya si es de la región) y estatus NOM-059."
                response = model.generate_content([prompt, img])

                st.success("Análisis completado")
                st.info(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
