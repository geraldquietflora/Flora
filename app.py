import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import requests

# 1. Configuración de seguridad (Usando tus Secrets de Streamlit)
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

def analizar_imagen_directo(img):
    try:
        # 2. Procesamiento de la imagen
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # 3. Preparación de la dirección (URL) y el paquete (Payload)
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Identifica esta planta de la Península de Yucatán. Responde solo con el nombre científico."},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }]
        }
        
        # 4. Envío de datos a Google
        response = requests.post(URL, json=payload, headers=headers)
        res_json = response.json()
        
        # 5. Extraer la respuesta de la IA
        texto_respuesta = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
        return texto_respuesta

    except Exception as e:
        return f"Error en el análisis: {str(e)}"

# --- Interfaz de la aplicación ---
st.title("🌿 Flora Yucatán IA")
st.write("Herramienta para identificación botánica en el campo.")

foto = st.camera_input("Captura la planta para identificar")

if foto:
    img = Image.open(foto)
    st.image(img, caption="Imagen capturada", use_column_width=True)
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Consultando con la base de datos..."):
            resultado = analizar_imagen_directo(img)
            st.success(f"Resultado: {resultado}")
