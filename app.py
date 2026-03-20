import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de página
st.set_page_config(page_title="Flora ID", layout="centered")

# Forzar configuración con la librería estable
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la API Key en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies.")

archivo = st.camera_input("Captura") or st.file_uploader("Sube imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 ANALIZAR"):
        with st.spinner('Procesando...'):
            try:
                # Usamos el modelo estable sin prefijos complejos
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                # Prompt optimizado para tu nivel de investigación
                prompt = (
                    "Identifica esta planta: Nombre científico, familia, "
                    "nombres comunes (incluye Maya), hábitat y estatus NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                
                st.success("Identificación exitosa")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Si el error persiste, verifica que la 'Generative Language API' esté HABILITADA en tu consola de Google Cloud.")
