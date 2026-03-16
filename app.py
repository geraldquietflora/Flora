import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# Recuperar la llave
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Error: Configura la llave en los Secrets.")
    st.stop()

API_KEY = st.secrets["GOOGLE_API_KEY"]

def identificar_planta(img):
    try:
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # CAMBIO DE MODELO: Usamos el modelo estable 'gemini-1.5-flash' sin sufijos
        # y forzamos la versión v1 de la API
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Eres un botánico experto. Identifica esta planta de la Península de Yucatán."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        res_json = response.json()
        
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # Si vuelve a fallar, el código imprimirá TODO lo que Google dice para ver el error real
            return f"Respuesta completa del servidor: {res_json}"
            
    except Exception as e:
        return f"Error técnico: {str(e)}"

st.title("🌿 Flora Yucatán IA")
foto = st.camera_input("Capturar")
archivo = st.file_uploader("Galería", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner("Probando conexión final..."):
            resultado = identificar_planta(img)
            st.success(f"Resultado:\n\n{resultado}")
