import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica para ECOSUR.")

# Configuración de API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")
    st.stop()

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Procesando imagen...'):
            try:
                # Usamos el modelo estable 1.5 Flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye nombres en Maya), "
                    "hábitat y estatus de conservación NOM-059/UICN."
                )
                
                response = model.generate_content([prompt, img])
                
                st.success("Análisis completado")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error detectado: {e}")
