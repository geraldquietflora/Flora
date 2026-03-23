import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# Conexión con los Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API Key en los Secrets de Streamlit.")
    st.stop()

archivo = st.camera_input("Capturar planta")

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Identificando...'):
            try:
                # Usamos el nombre técnico que sí reconoce la librería
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = "Actúa como un botánico experto de ECOSUR. Identifica esta planta: Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                
                response = model.generate_content([prompt, img])
                st.success("¡Logrado!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
