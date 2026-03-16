import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Error: Configura la llave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

API_KEY = st.secrets["GOOGLE_API_KEY"]

def identificar_planta(img):
    try:
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # URL ACTUALIZADA: Usamos v1 (Estable) y el modelo flash-001 que es el de largo plazo
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
        elif 'error' in res_json:
            # Si vuelve a fallar el nombre, intentamos con el modelo genérico
            return f"Error detallado de Google: {res_json['error']['message']}"
        else:
            return f"Respuesta inesperada: {res_json}"
            
    except Exception as e:
        return f"Error en la aplicación: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")
st.write("Identificación botánica de precisión.")

foto = st.camera_input("Capturar planta")
archivo = st.file_uploader("O cargar imagen", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner("Consultando servidores estables de Google..."):
            resultado = identificar_planta(img)
            st.markdown("### Resultado del Análisis:")
            st.info(resultado)
