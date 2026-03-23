import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# --- BLOQUE TÉCNICO PARA ELIMINAR EL ERROR 404 ---
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos a la librería a usar la versión estable 'v1'
    from google.generativeai import client
    client.DEFAULT_API_VERSION = "v1"
    
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura la API Key en los Secrets.")
    st.stop()
# ------------------------------------------------

# Interfaz con ambas opciones (Cámara y Galería)
st.write("### Captura o selecciona una imagen")
foto_camara = st.camera_input("Tomar foto")
foto_archivo = st.file_uploader("O subir archivo", type=["jpg", "png", "jpeg"])

archivo_final = foto_camara if foto_camara is not None else foto_archivo

if archivo_final:
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner('Procesando con el motor de producción...'):
            try:
                # Usamos el modelo estable
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo_final)
                
                prompt = (
                    "Actúa como un botánico experto de la Península de Yucatán. Identifica esta planta: "
                    "Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                st.success("¡Identificación completada!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")
