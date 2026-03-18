import streamlit as st
from google import genai
from PIL import Image
import io

# Configuración de la página
st.set_page_config(page_title="Flora - Identificador de Plantas", layout="centered")

st.title("🌿 Flora: Identificación de Plantas")
st.write("Sube una foto para analizar la especie y sus características.")

# Inicialización del cliente de Gemini usando Secrets de Streamlit
# Asegúrate de tener GOOGLE_API_KEY en Settings > Secrets de Streamlit Cloud
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Error de configuración: No se encontró la API Key en los Secrets.")
    st.stop()

# Selector de archivos
uploaded_file = st.file_uploader("Elige una imagen de una planta...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mostrar la imagen cargada
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen cargada', use_container_width=True)
    
    # Botón para analizar
    if st.button("Identificar Planta"):
        with st.spinner('Analizando con Gemini...'):
            try:
                # Usamos el modelo flash que es más rápido y eficiente para identificación
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[
                        "Actúa como un experto en botánica. Identifica esta planta, dime su nombre científico, "
                        "nombre común, hábitat natural y cuidados básicos si es una planta de jardín.",
                        image
                    ]
                )
                
                st.subheader("Resultados del Análisis:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Hubo un error al procesar la imagen: {e}")

# Pie de página
st.markdown("---")
st.caption("Desarrollado con Gemini 2.0 Flash API")
