import streamlit as st
from google import genai
from PIL import Image
import io

# 1. Configuración de la interfaz (Nombre de función corregido)
st.set_page_config(
    page_title="Flora - Identificador Botánico",
    page_icon="🌿",
    layout="centered"
)

# Estilos para mejorar la apariencia en dispositivos móviles
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #2e7d32; color: white; font-weight: bold; }
    .stCamera { border: 2px solid #2e7d32; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Flora: Análisis Botánico")
st.write("Herramienta de identificación asistida por IA para investigación y campo.")

# 2. Conexión con la API (Nueva librería google-genai)
try:
    # Recuerda configurar GOOGLE_API_KEY en Settings > Secrets de Streamlit Cloud
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

# 4. Procesamiento y Análisis Científico
if archivo_imagen is not None:
    # Vista previa para archivos subidos
    if opcion == "📁 Galería/Archivo":
        img_display = Image.open(archivo_imagen)
        st.image(img_display, caption="Imagen seleccionada", use_container_width=True)

    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner('Consultando base de datos botánica...'):
            try:
                # Abrimos la imagen para el modelo
                img_analizar = Image.open(archivo_imagen)
                
                # Prompt optimizado para tu perfil de investigador
                prompt_cientifico = (
                    "Actúa como un botánico experto en flora neotropical. "
                    "Analiza la imagen y proporciona: "
                    "1. Nombre científico y familia botánica. "
                    "2. Nombres comunes (incluyendo nombres en Maya si es nativa de la región). "
                    "3. Hábitat típico y distribución geográfica. "
                    "4. Características morfológicas clave para su identificación. "
                    "5. Importancia ecológica o estatus de conservación (NOM-059/UICN)."
                )

                # Usamos Gemini 1.5 Flash por ser el más estable en cuota gratuita
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt_cientifico, img_analizar]
                )

                st.success("Análisis Botánico Completado")
                st.markdown("### Ficha Técnica")
                st.info(response.text)

            except Exception as e:
                # Manejo amigable del error de cuota (429)
                if "429" in str(e):
                    st.warning("⏳ **Límite de cuota alcanzado:** Google ha restringido las peticiones gratuitas momentáneamente. Por favor, intenta de nuevo en unos minutos.")
                else:
                    st.error(f"Error en la comunicación con la API: {e}")

# Pie de página
st.markdown("---")
st.caption("Investigación y Desarrollo | Gemini 1.5 Flash API")
