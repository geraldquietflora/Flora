import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 2. Configuración de API Key desde Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Error: No se encontró la API KEY en los Secrets de Streamlit.")
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
                    {
                        "text": (
                            "Actúa como un botánico experto en la flora de la Península de Yucatán. "
                            "Describe brevemente qué planta ves y proporciona su nombre científico y común. "
                            "Si la imagen no es clara, da tu mejor estimación basada en las características visibles."
                        )
                    },
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
            return "La IA no pudo procesar la imagen. Intenta con una toma más clara o con mejor luz."

    except Exception as e:
        return f"Error técnico: {str(e)}"

# --- Interfaz de Usuario ---
st.title("🌿 Flora Yucatán IA")
st.write("Herramienta de identificación botánica regional.")

# Entradas de imagen
foto = st.camera_input("Capturar con la cámara")
archivo = st.file_uploader("O subir desde la galería", type=['jpg', 'jpeg', 'png'])

# Lógica de selección
imagen_final = foto if foto is not None else archivo

if imagen_final:
    img = Image.open(imagen_final)
    st.image(img, caption="Imagen para análisis", use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Consultando base de datos botánica..."):
            resultado = analizar_imagen_directo(img)
            st.success(f"Resultado:\n\n{resultado}")

st.divider()
st.info("Desarrollado para apoyo en investigación y campo.")
