import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# 1. Configuración de API (Forzamos la ruta estable)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets.")
    st.stop()

archivo = st.camera_input("Capturar planta")

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Procesando con el motor estable...'):
            try:
                # Cambiamos el nombre al identificador técnico universal
                # 'gemini-1.5-flash' es el motor que impulsa a Gemini 3 actualmente en la API
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                img = Image.open(archivo)
                prompt = (
                    "Actúa como un botánico experto de ECOSUR. Identifica esta planta: "
                    "Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("¡Análisis completado!")
                    st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Si el error persiste, verifica que la API Key en los Secrets sea la correcta.")
