import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# 1. Obtener la llave desde Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets.")
    st.stop()

# 2. Interfaz con Cámara + Subida de Archivos
st.write("### Captura o selecciona una imagen")
foto = st.camera_input("Tomar foto") or st.file_uploader("O seleccionar de galería", type=["jpg", "png", "jpeg"])

if foto:
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner('Comunicación directa con el motor de IA...'):
            try:
                # Convertir imagen a Base64
                img = Image.open(foto)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # URL DE PRODUCCIÓN FORZADA (v1) - Aquí se elimina el error 404
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Actúa como botánico experto de ECOSUR. Identifica esta planta: Nombre científico, familia, nombres comunes (Maya) y estatus NOM-059."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_str}}
                        ]
                    }]
                }

                # Petición directa al servidor de Google
                response = requests.post(url, json=payload)
                res_json = response.json()

                if response.status_code == 200:
                    resultado = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success("¡Identificación completada con éxito!")
                    st.markdown("---")
                    st.markdown(resultado)
                else:
                    st.error(f"Error de Google (Código {response.status_code}): {res_json.get('error', {}).get('message', 'Error desconocido')}")

            except Exception as e:
                st.error(f"Error técnico: {e}")
