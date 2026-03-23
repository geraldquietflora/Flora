import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

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
        with st.spinner('Detectando el mejor motor disponible...'):
            try:
                # 1. PREPARAR IMAGEN
                img = Image.open(foto)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # 2. AUTO-DETECCIÓN DE MODELO (Para evitar el 404)
                models_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
                models_resp = requests.get(models_url).json()
                
                # Buscamos el mejor modelo de visión disponible en tu cuenta
                available_models = [m['name'] for m in models_resp.get('models', []) 
                                   if 'generateContent' in m.get('supportedGenerationMethods', []) 
                                   and ('flash' in m['name'] or 'pro' in m['name'])]
                
                if not available_models:
                    st.error("No se encontraron modelos compatibles en tu cuenta.")
                    st.stop()
                
                # Usamos el primero de la lista (el más actualizado que Google te asigne)
                selected_model = available_models[0]
                
                # 3. PETICIÓN DE CONTENIDO
                url = f"https://generativelanguage.googleapis.com/v1/{selected_model}:generateContent?key={api_key}"
                
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
                    st.success(f"Identificado con {selected_model}")
                    st.markdown("---")
                    st.markdown(resultado)
                else:
                    st.error(f"Error {response.status_code}: {res_json}")

            except Exception as e:
                st.error(f"Error técnico: {e}")
