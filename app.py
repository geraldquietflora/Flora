import streamlit as st
from google import genai
from PIL import Image
import io

# --- CONFIGURACIÓN CORRECTA DE LA PÁGINA ---
st.set_page_config(page_title="Flora - Identificador de Plantas", layout="centered")

st.title("🌿 Flora: Identificación de Plantas")
st.write("Toma una foto o sube un archivo para analizar la especie.")

# Inicialización del cliente de Gemini
try:
    # Asegúrate de que la clave esté en Settings > Secrets de Streamlit Cloud
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Error de configuración: Revisa los Secrets en Streamlit Cloud.")
    st.stop()

# --- OPCIONES DE ENTRADA ---
opcion = st.radio("Selecciona fuente de imagen:", ["Cámara", "Subir Archivo"], horizontal=True)

uploaded_file = None

if opcion == "Cámara":
    # Este componente abre la cámara directamente en móviles y laptops
    uploaded_file = st.camera_input("Toma una foto de la planta")
else:
    # Opción para archivos guardados
    uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])

# --- PROCESAMIENTO ---
if uploaded_file is not None:
    # Abrir la imagen con Pillow
    image = Image.open(uploaded_file)
    
    # Mostrar vista previa solo si es archivo subido (camera_input ya la muestra)
    if opcion == "Subir Archivo":
        st.image(image, caption='Imagen cargada', use_container_width=True)
    
    if st.button("Identificar Planta"):
        with st.spinner('Analizando con Gemini 2.0 Flash...'):
            try:
                # El nuevo método de la librería google-genai
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[
                        "Actúa como un experto en botánica. Identifica esta planta, dime su nombre científico, "
                        "familia, hábitat natural y si es nativa de la región neotropical.",
                        image
                    ]
                )
                st.success("Análisis completo")
                st.markdown(f"### Resultado:\n{response.text}")
            except Exception as e:
                st.error(f"Error al conectar con la API: {e}")

# Pie de página
st.markdown("---")
st.caption("Desarrollado con Gemini 2.0 Flash API")
