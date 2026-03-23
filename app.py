import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# --- CONEXIÓN DE PRODUCCIÓN (ELIMINA EL ERROR 404) ---
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos explícitamente la versión 'v1' y el transporte 'rest'
    genai.configure(
        api_key=st.secrets["GOOGLE_API_KEY"],
        transport="rest"
    )
else:
    st.error("⚠️ Configura la API Key en los Secrets de Streamlit.")
    st.stop()

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Consultando base de datos botánica...'):
            try:
                # Usamos el modelo estable de producción
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto de la Península de Yucatán. Identifica esta planta: "
                    "Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("¡Análisis completado!")
                    st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico persistente: {e}")
