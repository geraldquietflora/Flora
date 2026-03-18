import streamlit as st
from google import genai
from PIL import Image

# 1. Configuración de la aplicación (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="Flora - Identificador Botánico",
    page_icon="🌿",
    layout="centered"
)

# Estilos visuales para una interfaz limpia y profesional
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #2e7d32; color: white; font-weight: bold; }
    .stCamera { border: 2px solid #2e7d32; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Flora: Análisis Botánico")
st.write("Herramienta de identificación científica asistida por IA.")

# 2. Conexión con la API de Google Gemini (Librería google-genai)
try:
    # El código busca la llave en Settings > Secrets de Streamlit Cloud
    # Formato esperado en Secrets: GOOGLE_API_KEY = "tu_llave_aqui"
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("⚠️ Configuración requerida: Por favor, añade tu 'GOOGLE_API_KEY' en los Secrets de Streamlit Cloud.")
    st.stop()

# 3. Interfaz de captura de imagen
opcion = st.radio("Selecciona fuente de imagen:", ["📷 Cámara", "📁 Galería/Archivo"], horizontal=True)

archivo_imagen = None
if opcion == "📷 Cámara":
    archivo_imagen = st.camera_input("Toma una foto de la planta")
else:
    archivo_imagen = st.file_uploader("Sube un archivo de imagen", type=["jpg", "jpeg", "png"])

# 4. Procesamiento y Análisis Científico
if archivo_imagen is not None:
    # Vista previa si se sube un archivo (la cámara ya muestra su propia vista)
    if opcion == "📁 Galería/Archivo":
        img_preview = Image.open(archivo_imagen)
        st.image(img_preview, caption="Imagen seleccionada", use_container_width=True)

    if st.button("🔍 INICIAR IDENTIFICACIÓN"):
        with st.spinner('Analizando especie con Gemini 2.0 Flash...'):
            try:
                # Convertir archivo a objeto Image de Pillow
                img_analizar = Image.open(archivo_imagen)
                
                # Prompt estructurado para resultados de nivel investigación
                prompt_botanico = (
                    "Actúa como un botánico experto en flora neotropical. "
                    "Analiza la imagen y proporciona la siguiente información: "
                    "1. Nombre científico y familia botánica. "
                    "2. Nombres comunes (incluye nombres en Maya si es nativa de la región). "
                    "3. Hábitat típico y distribución geográfica. "
                    "4. Características morfológicas clave visibles. "
                    "5. Importancia ecológica o estatus de conservación (NOM-059 o UICN)."
                )

                # Llamada al modelo 2.0 Flash (estándar actual)
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt_botanico, img_analizar]
                )

                st.success("Análisis Botánico Completado")
                st.markdown("### Ficha Técnica de la Especie")
                st.info(response.text)

            except Exception as e:
                # Manejo de errores amigable
                if "429" in str(e):
                    st.warning("⏳ Cuota excedida: Google ha limitado las peticiones gratuitas por ahora. Intenta de nuevo en unos minutos.")
                elif "403" in str(e):
                    st.error("🚫 Error 403: Tu API Key ha sido bloqueada o reportada como filtrada. Genera una nueva en Google AI Studio.")
                else:
                    st.error(f"Error técnico en la comunicación: {e}")

# Pie de página
st.markdown("---")
st.caption("Investigación y Desarrollo | Gemini 2.0 Flash API")
