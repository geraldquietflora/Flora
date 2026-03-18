import streamlit as st
from google import genai
from PIL import Image
import io

# 1. Configuración de la interfaz
st.set_page_config(
    page_title="Flora - Identificador Botánico",
    page_icon="🌿",
    layout="centered"
)

# Estilos visuales
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #2e7d32; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Flora: Análisis Botánico")
st.write("Herramienta de identificación asistida por IA.")

# 2. Conexión con la API
try:
    # Configura tu clave en Settings > Secrets de Streamlit Cloud
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("⚠️ Error: No se detecta la API Key en los Secrets de Streamlit.")
    st.stop()

# 3. Selección de entrada de imagen
opcion = st.radio("Fuente de la imagen:", ["📷 Cámara", "📁 Galería/Archivo"], horizontal=True)

archivo_imagen = None
if opcion == "📷 Cámara":
    archivo_imagen = st.camera_input("Captura la planta")
else:
    archivo_imagen = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

# 4. Procesamiento
if archivo_imagen is not None:
    if opcion == "📁 Galería/Archivo":
        img_display = Image.open(archivo_imagen)
        st.image(img_display, caption="Imagen seleccionada", use_container_width=True)

    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner('Consultando base de datos...'):
            try:
                img_analizar = Image.open(archivo_imagen)
                
                # Prompt para resultados científicos
                prompt_cientifico = (
                    "Actúa como un botánico experto. Identifica la planta de la imagen y proporciona: "
                    "Nombre científico, familia, nombres comunes, hábitat y estatus de conservación."
                )

                # CAMBIO CLAVE: Usamos gemini-2.0-flash que es el estándar actual para esta librería
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=[prompt_cientifico, img_analizar]
                )

                st.success("Análisis Completado")
                st.info(response.text)

            except Exception as e:
                # Si el error persiste, el mensaje nos dirá exactamente qué modelo prefiere la API
                st.error(f"Error en la comunicación con la API: {e}")

# Pie de página
st.markdown("---")
st.caption("Investigación y Desarrollo | Gemini 2.0 Flash API")
