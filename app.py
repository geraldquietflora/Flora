import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# Recuperar la nueva llave desde Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Error: Configura la nueva llave en los Secrets de Streamlit.")
    st.stop()

API_KEY = st.secrets["GOOGLE_API_KEY"]

def identificar_planta(img):
    try:
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # Usamos la URL v1beta con el modelo latest
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Actúa como un botánico experto de la Península de Yucatán. Identifica la planta de la foto: Nombre científico, común y descripción breve."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        res_json = response.json()
        
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {res_json.get('error', {}).get('message', 'Respuesta vacía')}"
            
    except Exception as e:
        return f"Error técnico: {str(e)}"

st.title("🌿 Flora Yucatán IA")
foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("O cargar imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner("Analizando con la nueva llave..."):
            resultado = identificar_planta(img)
            st.success(f"Resultado:\n\n{resultado}")
