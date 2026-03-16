import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# Configuración de API Key
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Error: Revisa la API KEY en Secrets.")
    st.stop()

def analizar_imagen_directo(img):
    try:
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # CAMBIO CLAVE: Usamos la versión 'v1' estable
        URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Eres un botánico experto en la Península de Yucatán. Identifica la planta de esta foto (nombre científico y común). Describe brevemente sus características."},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }]
        }
        
        response = requests.post(URL, json=payload, headers=headers)
        res_json = response.json()
        
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
        elif 'error' in res_json:
            return f"Error de Google: {res_json['error']['message']}"
        else:
            return "No se pudo generar una respuesta. Intenta con otra foto."

    except Exception as e:
        return f"Error técnico: {str(e)}"

# Interfaz simplificada
st.title("🌿 Flora Yucatán IA")
st.write("Identificación botánica regional.")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("O cargar desde galería", type=['jpg', 'jpeg', 'png'])

imagen_final = foto if foto is not None else archivo

if imagen_final:
    img = Image.open(imagen_final)
    st.image(img, use_container_width=True)
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Analizando con Gemini 1.5 Flash..."):
            resultado = analizar_imagen_directo(img)
            st.success(f"Resultado:\n\n{resultado}")
