import streamlit as st
import google.generativeai as genai
from PIL import Image
from google.generativeai.types import RequestOptions

# 1. Configuración de la página
st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies (Modo Producción v1).")

# 2. Validación de API Key en Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Configuración de la librería
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Conectando con servidores de producción de Google...'):
            try:
                # Inicializamos el modelo estable
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye nombres en Maya), "
                    "hábitat y estatus de conservación NOM-059/UICN."
                )
                
                # LA SOLUCIÓN AL ERROR 404: Forzar versión v1 mediante RequestOptions
                response = model.generate_content(
                    [prompt, img],
                    request_options=RequestOptions(api_version='v1')
                )
                
                st.success("Análisis exitoso")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Si el error 404 persiste, asegúrate de haber actualizado la API Key en los Secrets con la nueva que generaste en Google Cloud.")
