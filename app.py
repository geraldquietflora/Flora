import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets.")
    st.stop()

st.write("### Captura o selecciona una imagen")
foto = st.camera_input("Tomar foto") or st.file_uploader("O subir archivo", type=["jpg", "png", "jpeg"])

if foto:
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner('Conectando con el motor de visión estable...'):
            try:
                # Procesamiento de imagen
                img = Image.open(foto)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # CAMBIO CLAVE: Usamos el modelo Pro Vision que es el estándar en v1
                model_name = "gemini-pro-vision" 
                url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Actúa como botánico experto de ECOSUR. Identifica esta planta: Nombre científico, familia, nombres comunes (incluyendo Maya) y estatus NOM-059."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_str}}
                        ]
                    }]
                }

                response = requests.post(url, json=payload)
                res_json = response.json()

                if response.status_code == 200:
                    resultado = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success("¡Identificación completada!")
                    st.markdown("---")
                    st.markdown(resultado)
                else:
                    # Si falla el Pro Vision, intentamos con el 1.5 pero con la ruta correcta
                    st.error(f"Error {response.status_code}: {res_json.get('error', {}).get('message')}")
                    st.info("Sugerencia: Cambia 'gemini-pro-vision' por 'gemini-1.5-flash-latest' en el código.")

            except Exception as e:
                st.error(f"Error técnico: {e}")
