import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# Nueva forma de configurar Gemini en 2026
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura la API Key en los Secrets (borra el ejemplo anterior).")
    st.stop()

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Identificando con Gemini 3 Flash...'):
            try:
                img = Image.open(archivo)
                
                # Llamada al modelo Gemini 3 Flash
                response = client.models.generate_content(
                    model="gemini-3-flash",
                    contents=["Actúa como botánico experto de ECOSUR. Identifica: Nombre científico, familia, nombres en Maya y estatus NOM-059.", img]
                )
                
                st.success("¡Identificación exitosa!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
