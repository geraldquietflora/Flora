import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import requests

# 1. Configuración de seguridad (Usa tu llave guardada en Secrets)
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

def analizar_imagen_directo(img):
    try:
        # Procesamiento de la imagen para enviarla a la IA
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # URL de conexión con el modelo Gemini de Google
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        # Instrucciones para la IA (Prompt)
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Identifica esta planta de la Península de Yucatán. Responde solo con el nombre científico y el nombre común local si existe."},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }]
        }
        
        # Petición a los servidores de Google
        response = requests.post(URL, json=payload, headers=headers)
        res_json = response.json()
        
        # Extraer el texto de la respuesta
        texto_respuesta = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
        return texto_respuesta

    except Exception as e:
        return f"Error en el análisis: {str(e)}"

# --- INTERFAZ DE LA APLICACIÓN ---
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")
st.title("🌿 Flora Yucatán IA")
st.write("Herramienta de identificación botánica para la Península de Yucatán.")

# OPCIÓN 1: Cámara en vivo
foto = st.camera_input("Capturar con la cámara")

# OPCIÓN 2: Subir archivo de la galería
archivo = st.file_uploader("O selecciona una imagen de tu dispositivo", type=['jpg', 'jpeg', 'png'])

# Lógica para decidir qué imagen analizar
imagen_final = None
if foto is not None:
    imagen_final = foto
elif archivo is not None:
    imagen_final = archivo

# Si hay una imagen (ya sea de cámara o archivo), mostrarla y dar opción de identificar
if imagen_final:
    img = Image.open(imagen_final)
    st.image(img, caption="Imagen cargada correctamente", use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Analizando la imagen con la base de datos de Google..."):
            resultado = analizar_imagen_directo(img)
            st.success(f"Resultado: {resultado}")

# Información institucional
st.markdown("---")
st.info("Desarrollado para asistencia en identificación botánica regional.")
