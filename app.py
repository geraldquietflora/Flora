import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración básica
st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies.")

# Configuración de la API forzando transporte REST (evita el error 404 v1beta)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# ESTA ES LA LÍNEA CRUCIAL
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')

archivo = st.camera_input("Capturar") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 ANALIZAR"):
        with st.spinner('Conectando con Google Cloud...'):
            try:
                # Usamos el modelo estable
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Identifica esta planta: Nombre científico, familia, "
                    "nombres comunes (incluye Maya), hábitat y estatus NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                
                st.success("Análisis exitoso")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
