import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Configuración de la página
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 2. Forzar la versión de la API y configurar el modelo
try:
    # ESTA LÍNEA ES CRÍTICA: Forzamos a que NO use v1beta
    os.environ["GOOGLE_API_VERSION"] = "v1"
    
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Intentamos con el modelo Pro, que suele ser más estable en estos cambios de versión
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

def analizar_con_libreria(img):
    try:
        instruccion = (
            "Eres un botánico experto en la Península de Yucatán. "
            "Identifica esta planta: nombre científico, nombre común y descripción breve. "
            "Si no estás seguro, da tu mejor hipótesis basada en la morfología visible."
        )
        
        response = model.generate_content([instruccion, img])
        return response.text
    except Exception as e:
        # Si el modelo Pro falla, intentamos automáticamente con el Flash por si acaso
        try:
            model_flash = genai.GenerativeModel('gemini-1.5-flash')
            response = model_flash.generate_content([instruccion, img])
            return response.text
        except:
            return f"Error persistente de conexión con Google: {str(e)}. Por favor, intenta de nuevo en unos minutos."

# --- Interfaz de Usuario ---
st.title("🌿 Flora Yucatán IA")
st.write("Identificación botánica profesional.")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("O cargar imagen", type=['jpg', 'jpeg', 'png'])

imagen_final = foto if foto is not None else archivo

if imagen_final:
    img = Image.open(imagen_final)
    st.image(img, use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Consultando servidores de Google (v1)..."):
            resultado = analizar_con_libreria(img)
            st.success(f"Resultado:\n\n{resultado}")

st.divider()
st.info("Desarrollado para el estudio de la biodiversidad regional.")
