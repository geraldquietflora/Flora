import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="Flora - Identificador Botánico", layout="centered", page_icon="🌿")

# Estilo para el botón de análisis
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #2e7d32; color: white; font-weight: bold; height: 3.5em; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica asistida por IA para investigadores.")

# 2. Configuración de la API con la librería estable
try:
    # Busca la clave en Settings > Secrets de Streamlit Cloud
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Interfaz de usuario
opcion = st.radio("Fuente de imagen:", ["📷 Cámara", "📁 Archivo"], horizontal=True)
archivo = st.camera_input("Capturar") if opcion == "📷 Cámara" else st.file_uploader("Sube imagen", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    if opcion == "📁 Archivo":
        st.image(img, use_container_width=True)

    if st.button("🔍 INICIAR IDENTIFICACIÓN"):
        with st.spinner('Consultando base de datos botánica...'):
            try:
                # Usamos el modelo estable 1.5 Flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluyendo nombres en Maya si es de la región), "
                    "distribución neotropical y estatus de conservación (NOM-059/UICN)."
                )

                # Generar contenido (formato compatible con la librería estable)
                response = model.generate_content([prompt, img])
                
                st.success("Análisis completado")
                st.markdown(f"### Ficha Técnica:\n{response.text}")

            except Exception as e:
                if "429" in str(e):
                    st.warning("⏳ Cuota excedida. Tu tarjeta está activa, pero Google puede tardar hasta 48h en liberar los límites totales. Reintenta en unos minutos.")
                else:
                    st.error(f"Detalle técnico del error: {e}")

st.divider()
st.caption("Investigación Científica | ECOSUR Chetumal")
