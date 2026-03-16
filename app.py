import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 2. Configuración de la IA con la librería oficial
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Inicializamos el modelo directamente
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

def analizar_con_libreria(img):
    try:
        # La librería de Google acepta la imagen de PIL directamente
        instruccion = "Actúa como un botánico experto. Identifica esta planta de la Península de Yucatán. Dame nombre científico, común y una breve descripción."
        
        response = model.generate_content([instruccion, img])
        return response.text
    except Exception as e:
        return f"Error al analizar: {str(e)}"

# --- Interfaz de Usuario ---
st.title("🌿 Flora Yucatán IA")
st.write("Identificación botánica de precisión.")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("O cargar imagen", type=['jpg', 'jpeg', 'png'])

imagen_final = foto if foto is not None else archivo

if imagen_final:
    img = Image.open(imagen_final)
    st.image(img, use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Consultando experto botánico virtual..."):
            resultado = analizar_con_libreria(img)
            st.success(f"Resultado:\n\n{resultado}")

st.divider()
st.info("Herramienta académica para el estudio de la biodiversidad regional.")
