import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies (Modo Producción).")

# 1. Configuración de API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# ESTA CONFIGURACIÓN FUERZA LA VERSIÓN DE PRODUCCIÓN
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

archivo = st.camera_input("Capturar") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Conectando con servidores de producción de Google...'):
            try:
                # Especificamos el modelo estándar
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye Maya), "
                    "hábitat y estatus de conservación NOM-059."
                )
                
                # FORZAMOS LA VERSIÓN V1 EN LA PETICIÓN
                response = model.generate_content(
                    [prompt, img],
                    request_options={"api_version": "v1"}
                )
                
                st.success("Análisis exitoso")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error persistente: {e}")
                st.info("Nota: Si el error 404 persiste, es posible que Streamlit no haya actualizado el código. Intenta un 'Reboot' desde el panel.")
