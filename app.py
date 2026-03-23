import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# 1. Configuración de API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura la API Key en los Secrets de Streamlit.")
    st.stop()

# 2. Interfaz Doble (Cámara y Galería)
st.write("### Captura o selecciona una imagen")
foto_camara = st.camera_input("Tomar foto con la cámara")
foto_galeria = st.file_uploader("O elige una imagen de tu dispositivo", type=["jpg", "png", "jpeg"])

# Usar cualquiera de las dos que esté disponible
archivo = foto_camara or foto_galeria

if archivo:
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner('Consultando base de datos botánica...'):
            try:
                # Modelo gemini-1.5-flash es el estándar estable
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto de la Península de Yucatán. Identifica esta planta: "
                    "Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                st.success("¡Análisis completado!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
