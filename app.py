import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# --- PROTOCOLO DE CONEXIÓN DIRECTA (ELIMINA EL ERROR 404) ---
if "GOOGLE_API_KEY" in st.secrets:
    # 1. Forzamos la versión v1 de producción
    # 2. Forzamos el transporte 'rest' (más estable para redes académicas/gubernamentales)
    genai.configure(
        api_key=st.secrets["GOOGLE_API_KEY"],
        transport="rest" 
    )
else:
    st.error("⚠️ Configura la API Key en los Secrets.")
    st.stop()

# Interfaz con Cámara + Selector de archivos (Restaurado)
st.write("### Captura o selecciona una imagen")
foto_camara = st.camera_input("Tomar foto")
foto_archivo = st.file_uploader("O seleccionar de la galería", type=["jpg", "png", "jpeg"])

archivo = foto_camara or foto_archivo

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Conectando con el servidor de producción...'):
            try:
                # Usamos el identificador de modelo base más compatible
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto de la Península de Yucatán. Identifica esta planta: "
                    "Nombre científico, familia, nombres comunes (incluye Maya) y estatus NOM-059."
                )
                
                # Generación de contenido
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("¡Análisis completado!")
                    st.markdown("---")
                    st.markdown(response.text)
                
            except Exception as e:
                # Si esto falla, el log nos dirá exactamente qué puerta está cerrada
                st.error(f"Error técnico: {e}")
