import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# Configuración de API
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos el uso de la versión de producción v1
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Revisa los Secrets.")
    st.stop()

archivo = st.camera_input("Capturar") or st.file_uploader("Subir", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 ANALIZAR"):
        with st.spinner('Conectando con Google Cloud...'):
            try:
                # CAMBIO CLAVE: Especificamos el modelo con su ruta completa de producción
                # Esto suele saltarse el error 404 de la versión beta
                model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                
                img = Image.open(archivo)
                prompt = "Identifica esta planta: Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                
                # Intentamos la generación
                response = model.generate_content([prompt, img])
                
                st.success("Análisis exitoso")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Si el error 404 persiste, revisa en Google Cloud Console que 'Generative Language API' no tenga restricciones de cuota.")
