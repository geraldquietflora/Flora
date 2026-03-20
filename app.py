import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies.")

# 2. Configuración simple de la API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Interfaz de usuario
archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Procesando...'):
            try:
                # Usamos el modelo 1.5 Flash (el más estable para visión)
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye Maya), "
                    "hábitat y estatus de conservación NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                
                st.success("Análisis completado")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error de comunicación: {e}")
