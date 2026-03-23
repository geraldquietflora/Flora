import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# --- BLOQUE ANTIVIRUS PARA EL ERROR 404 ---
if "GOOGLE_API_KEY" in st.secrets:
    # 1. Forzamos la configuración de la API
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # 2. HACK DEFINITIVO: Forzamos la ruta de producción 'v1' manualmente
    # Esto sobreescribe cualquier intento de la librería de ir a 'v1beta'
    from google.generativeai import client
    client.DEFAULT_API_VERSION = "v1" 
else:
    st.error("⚠️ Configura la API Key en los Secrets.")
    st.stop()
# ------------------------------------------

st.write("### Captura o selecciona una imagen")
foto_camara = st.camera_input("Tomar foto")
foto_archivo = st.file_uploader("O subir desde galería", type=["jpg", "png", "jpeg"])

archivo = foto_camara or foto_archivo

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Forzando conexión segura con el motor estable...'):
            try:
                # Usamos el modelo sin el prefijo 'models/' para evitar que la URL se rompa
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto de la Península de Yucatán. Identifica esta planta: "
                    "Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                )
                
                response = model.generate_content([prompt, img])
                st.success("¡Lo logramos!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # Si falla, imprimimos la URL que está intentando usar para diagnosticar
                st.error(f"Error persistente: {e}")
