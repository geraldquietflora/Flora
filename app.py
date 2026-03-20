import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# 1. Configuración con Gemini 3
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets.")
    st.stop()

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Analizando con Gemini 3 Flash...'):
            try:
                # REGRESAMOS AL MODELO QUE TE FUNCIONÓ
                model = genai.GenerativeModel('gemini-3-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye nombres en Maya), "
                    "hábitat y estatus de conservación NOM-059/UICN."
                )
                
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("¡Análisis completado!")
                    st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error de conexión: {e}")
                st.info("Asegúrate de que la API Key en los Secrets sea la correcta.")
