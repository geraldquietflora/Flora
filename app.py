import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def encontrar_mejor_modelo():
    """Busca dinámicamente qué modelo de visión tienes activo."""
    try:
        modelos = genai.list_models()
        # Buscamos modelos que soporten imágenes (generación de contenido)
        for m in modelos:
            if 'generateContent' in m.supported_generation_methods:
                # Prioridad 1: Gemini 3 (el que viste en tu pantalla)
                if 'gemini-3-flash' in m.name:
                    return m.name
                # Prioridad 2: Gemini 1.5 Flash
                if 'gemini-1.5-flash' in m.name:
                    return m.name
        # Si no encuentra esos, toma el primero que diga gemini
        for m in modelos:
            if 'gemini' in m.name:
                return m.name
    except Exception as e:
        st.error(f"Error al listar modelos: {e}")
    return None

def identificar(img):
    try:
        nombre_modelo = encontrar_mejor_modelo()
        if not nombre_modelo:
            return "No se encontraron modelos de IA activos en esta cuenta."
        
        # Mostramos qué modelo estamos usando para diagnóstico
        st.info(f"🔬 Conectado con: `{nombre_modelo}`")
        
        model = genai.GenerativeModel(nombre_modelo)
        prompt = "Identifica esta planta de la Península de Yucatán: nombre científico, común y descripción."
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Aviso del sistema: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("Subir imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 ANALIZAR ESPECIE"):
        with st.spinner("Buscando en la base de datos..."):
            resultado = identificar(img)
            st.success(resultado)

st.divider()
st.caption("Esta versión detecta automáticamente el modelo disponible en tu región.")
