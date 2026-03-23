import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración inicial
st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# Conexión con la API Key de los Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Interfaz: Cámara y Selector de Archivos (Tal como funcionaba)
st.write("### Captura o selecciona una imagen")
archivo_camara = st.camera_input("Tomar foto con la cámara")
archivo_galeria = st.file_uploader("O elige una imagen de tu dispositivo", type=["jpg", "png", "jpeg"])

# Selección de la fuente de imagen
archivo = archivo_camara or archivo_galeria

if archivo:
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner('Consultando al botánico virtual...'):
            try:
                # Usamos el modelo que funcionaba perfectamente antes de los errores 404
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto de la Península de Yucatán. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluyendo nombres en Maya) y estatus de conservación NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                
                st.success("¡Identificación completada!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
