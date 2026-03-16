import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import requests

# 1. Configuración de página (Debe ser lo primero después de los imports)
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 2. Configuración de seguridad segura
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Error con la API KEY en Secrets. Verifica que esté bien escrita.")
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
                    "text": "Actúa como un botánico experto en la Península de Yucatán. Describe brevemente lo que ves en la imagen e intenta identificar la especie (nombre científico y común). Si la imagen es borrosa, dame tu mejor estimación.",
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
        else:
            return "La IA no pudo procesar esta imagen. Intenta con una toma más clara."

    except Exception as e:
        return f"Error técnico: {str(e)}"

# --- Interfaz ---
st.title("🌿 Flora Yucatán IA")
st.write("Herramienta de identificación botánica.")

# Los dos métodos de entrada
foto = st.camera_input("Captura con la cámara")
archivo = st.file_uploader("O sube una imagen de tu galería", type=['jpg', 'jpeg', 'png'])

# Selección de imagen
imagen_final = foto if foto is not None else archivo

if imagen_final:
    img = Image.open(imagen_final)
    st.image(img, caption="Imagen cargada", use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Analizando..."):
            resultado = analizar_imagen_directo(img)
            st.success(f"Resultado: {resultado}")

st.divider()
st.info("Desarrollado para apoyo en identificación botánica regional.")
