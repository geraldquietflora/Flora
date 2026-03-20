import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración inicial
st.set_page_config(page_title="Flora - ID Botánico", layout="centered", page_icon="🌿")

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies vegetales.")

# 2. Configuración de la API (Librería estable)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Entrada de imagen
opcion = st.radio("Fuente:", ["📷 Cámara", "📁 Archivo"], horizontal=True)
archivo = st.camera_input("Capturar") if opcion == "📷 Cámara" else st.file_uploader("Sube imagen", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    if opcion == "📁 Archivo":
        st.image(img, use_container_width=True)

    if st.button("🔍 INICIAR IDENTIFICACIÓN"):
        with st.spinner('Analizando...'):
            try:
                # Usamos el modelo 1.5 Flash que es el más compatible
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye Maya), "
                    "distribución neotropical y estatus de conservación (NOM-059/UICN)."
                )

                # Generación de contenido
                response = model.generate_content([prompt, img])
                
                st.success("Análisis completado")
                st.markdown(f"### Resultado:\n{response.text}")

            except Exception as e:
                if "429" in str(e):
                    st.warning("⏳ Cuota excedida. Tu tarjeta en Google Cloud está activa, pero Google tarda hasta 48h en liberar los límites. Reintenta en unos minutos.")
                else:
                    st.error(f"Error técnico: {e}")

st.divider()
st.caption("Investigación Científica | ECOSUR")
