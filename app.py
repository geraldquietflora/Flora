import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. Configuración básica de la página
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 2. Validación de la API KEY
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Error: No se encontró la llave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

API_KEY = st.secrets["GOOGLE_API_KEY"]

def identificar_planta(img):
    try:
        # Procesar imagen para enviarla
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # PROTOTIPO DE URL ACTUALIZADO: v1beta con el modelo flash-latest
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": "Actúa como un botánico experto en la flora de la Península de Yucatán. Identifica la planta de esta foto. Dame el nombre científico, el nombre común y una descripción breve de sus características botánicas."
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }],
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }
        
        # Petición directa al servidor de Google
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        elif 'error' in res_json:
            return f"Error técnico de Google: {res_json['error']['message']}"
        else:
            return "La IA no pudo procesar esta imagen específica. Intenta con una toma más clara o con otra planta."
            
    except Exception as e:
        return f"Error en la aplicación: {str(e)}"

# --- INTERFAZ DE USUARIO ---
st.title("🌿 Flora Yucatán IA")
st.markdown("### Identificación Botánica con Inteligencia Artificial")
st.write("Herramienta diseñada para el estudio de la biodiversidad regional.")

# Opciones de entrada de imagen
foto = st.camera_input("Capturar con la cámara del dispositivo")
archivo = st.file_uploader("O cargar una imagen desde la galería", type=['jpg', 'jpeg', 'png'])

# Lógica para seleccionar la fuente de la imagen
img_input = foto if foto is not None else archivo

if img_input:
    # Mostrar la imagen cargada
    img = Image.open(img_input)
    st.image(img, caption="Muestra para análisis", use_container_width=True)
    
    # Botón de acción
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Analizando morfología botánica..."):
            resultado = identificar_planta(img)
            st.success("### Resultado del Análisis:")
