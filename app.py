import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

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
        
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Eres un botánico experto. Identifica la planta de esta foto (nombre científico y común). Si no estás seguro, describe lo que ves y da tu mejor hipótesis científica. No te guardes la respuesta por falta de claridad."},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }],
            # ESTO ES LO NUEVO: Bajamos los filtros de seguridad para que siempre responda
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }
        
        response = requests.post(URL, json=payload, headers=headers)
        res_json = response.json()
        
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
        elif 'error' in res_json:
            return f"Error de Google: {res_json['error']['message']}"
        else:
            return "La IA no pudo generar una descripción. Prueba con otra foto u otro ángulo."

    except Exception as e:
        return f"Error técnico: {str(e)}"

st.title("🌿 Flora Yucatán IA")
foto = st.camera_input("Capturar")
archivo = st.file_uploader("Galería", type=['jpg', 'jpeg', 'png'])

imagen_final = foto if foto is not None else archivo

if imagen_final:
    img = Image.open(imagen_final)
    st.image(img, use_container_width=True)
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner("Analizando..."):
            st.success(f"Resultado:\n\n{analizar_imagen_directo(img)}")
