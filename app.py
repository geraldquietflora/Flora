import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 1. Configuración de API Key
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Falta la API KEY en Secrets.")
    st.stop()

def identificar_planta(img):
    try:
        # Preparar la imagen
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # URL FORZADA a v1 (Estable) - Sin usar librerías intermedias
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Actúa como un botánico experto de la Península de Yucatán. Identifica la planta de la foto: Nombre científico, común y una breve descripción."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # Si Google devuelve un error, lo mostramos tal cual para saber qué pasa
            return f"Respuesta inesperada de Google: {res_json}"
            
    except Exception as e:
        return f"Error en el proceso: {str(e)}"

# --- Interfaz ---
st.title("🌿 Flora Yucatán IA")
st.write("Herramienta de identificación botánica.")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("O cargar imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner("Conectando directamente con el servidor v1..."):
            resultado = identificar_planta(img)
            st.success(f"Resultado:\n\n{resultado}")
