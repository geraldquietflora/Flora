import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave en los Secrets de Streamlit.")
    st.stop()

# Conexión inicial
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def obtener_modelo_valido():
    """Busca en tu cuenta qué modelos de visión tienes activos."""
    try:
        modelos = genai.list_models()
        # Buscamos modelos que soporten generación de contenido y tengan 'flash' o 'pro'
        for m in modelos:
            if 'generateContent' in m.supported_generation_methods:
                # Priorizamos el flash si existe, si no, cualquier gemini disponible
                if 'gemini-1.5-flash' in m.name:
                    return m.name
        # Si no encontró flash, agarra el primero que diga gemini
        for m in modelos:
            if 'gemini' in m.name:
                return m.name
    except Exception as e:
        st.error(f"Error al listar modelos: {e}")
    return None

def identificar(img):
    try:
        nombre_modelo = obtener_modelo_valido()
        if not nombre_modelo:
            return "No se encontraron modelos de IA disponibles en esta cuenta."
        
        st.write(f"🔬 Usando modelo: `{nombre_modelo}`")
        model = genai.GenerativeModel(nombre_modelo)
        
        prompt = "Identifica esta planta de la Península de Yucatán. Dame Nombre científico, Nombre común y una descripción breve."
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Error en el análisis: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")
st.write("Identificación botánica con selección automática de modelo.")

foto = st.camera_input("Capturar")
archivo = st.file_uploader("Galería", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 ANALIZAR ESPECIE"):
        with st.spinner("Escaneando servidores de Google..."):
            resultado = identificar(img)
            st.success(resultado)

st.divider()
st.info("Este código detecta automáticamente qué versión de Gemini tienes habilitada.")
