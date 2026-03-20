import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# 1. Validación de API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 2. Configuración de seguridad: Forzamos el transporte REST para evitar v1beta
genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"],
    transport="rest"
)

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Consultando base de datos de producción...'):
            try:
                # Especificamos el modelo de forma explícita
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                img = Image.open(archivo)
                
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye Maya), "
                    "hábitat y estatus de conservación NOM-059/UICN."
                )
                
                # La clave aquí es el parámetro request_options
                response = model.generate_content(
                    [prompt, img],
                    request_options={"api_version": "v1"}
                )
                
                st.success("Análisis completado")
                st.markdown(response.text)
                
            except Exception as e:
                # Si esto falla, el error nos dirá exactamente qué puerta está cerrada
                st.error(f"Error de comunicación: {e}")
