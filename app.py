import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. Configuración de la interfaz
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

# 2. Recuperar la llave de los Secrets (Panel de Streamlit Cloud)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ No se detectó la llave en Secrets. Verifica que el nombre sea GOOGLE_API_KEY.")
    st.stop()

def identificar_planta(img):
    try:
        # Preparación de la imagen
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # Endpoint estable de Google v1beta
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Identifica esta planta de la Península de Yucatán. Dame el nombre científico, el nombre común y una descripción breve de sus características botánicas."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        # Procesamiento de la respuesta
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        elif 'error' in res_json:
            return f"Error de Google: {res_json['error']['message']}"
        else:
            return "No se pudo obtener información de esta imagen. Intenta con otra toma."
            
    except Exception as e:
        return f"Error técnico: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")
st.write("Identificación botánica con Inteligencia Artificial.")

# Entrada de imagen
foto = st.camera_input("Capturar con la cámara")
archivo = st.file_uploader("O cargar desde galería", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Consultando al experto virtual..."):
            resultado = identificar_planta(img)
            st.success("### Resultado del Análisis:")
            st.write(resultado)

st.divider()
st.info("Herramienta desarrollada para apoyo en investigación y docencia.")
