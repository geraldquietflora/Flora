import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies (Acceso Directo v1).")

# 2. Validación de API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. CONFIGURACIÓN CORRECTA: Forzamos la versión v1 globalmente
# Esto elimina el error 404 v1beta sin causar errores de argumentos
from google.generativeai import client
client.DEFAULT_API_VERSION = "v1" 

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Conectando con servidores de producción...'):
            try:
                # Inicializamos el modelo de forma limpia
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye nombres en Maya), "
                    "hábitat y estatus de conservación NOM-059/UICN."
                )
                
                # La llamada ahora es simple, porque ya configuramos la versión arriba
                response = model.generate_content([prompt, img])
                
                st.success("Análisis exitoso")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Si el error persiste, asegúrate de que la API Key en Secrets sea la que generaste en la Consola de Google Cloud.")
