import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página y estética
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿", layout="centered")

# 2. Conexión con la API (Seguridad en Secrets)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def identificar_especie(img):
    try:
        # CAMBIO ESTRATÉGICO: Usamos 1.5 Flash para tener 1,500 intentos diarios
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Actúa como un botánico experto especializado en la Península de Yucatán. "
            "Analiza la imagen e identifica la planta. Proporciona: "
            "1. Nombre científico (en cursivas). "
            "2. Nombre común regional. "
            "3. Familia botánica. "
            "4. Descripción breve de sus rasgos clave y su importancia ecológica en la región."
        )
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Aviso del sistema: {str(e)}"

# --- INTERFAZ DE USUARIO ---
st.title("🌿 Flora Yucatán IA")
st.markdown("### Identificación Botánica Profesional (v1.5 Flash)")
st.write("Herramienta optimizada para investigación y monitoreo biológico.")

# Captura de datos
foto = st.camera_input("Capturar con la cámara del dispositivo")
archivo = st.file_uploader("O cargar desde la galería", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    # Procesamiento de imagen
    img = Image.open(img_input)
    st.image(img, caption="Muestra para análisis", use_container_width=True)
    
    if st.button("🔍 INICIAR IDENTIFICACIÓN"):
        with st.spinner("Consultando base de datos botánica..."):
            resultado = identificar_especie(img)
            st.divider()
            st.markdown("### Resultado del Análisis:")
            st.success(resultado)

st.divider()
st.caption("Desarrollado para el apoyo a la investigación en el Sureste de México. Limite: 1,500 consultas/día.")
