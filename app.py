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
        
        # URL estable v1beta
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Identifica esta planta de la Península de Yucatán. Dame nombre científico, común y descripción."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        # --- NUEVA LÓGICA DE EXTRACCIÓN ROBUSTA ---
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            candidate = res_json['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                return candidate['content']['parts'][0]['text']
            else:
                return f"Google no generó texto. Razón de bloqueo: {candidate.get('finishReason', 'Desconocida')}"
        elif 'error' in res_json:
            return f"Error de la API: {res_json['error']['message']}"
        else:
            return f"Respuesta cruda del servidor: {res_json}"
            
    except Exception as e:
        return f"Error en la aplicación: {str(e)}"

# --- INTERFAZ ---
st.title("🌿 Flora Yucatán IA")
foto = st.camera_input("Capturar")
archivo = st.file_uploader("Galería", type=['jpg', 'jpeg', 'png'])

img_input = foto if foto is not None else archivo

if img_input:
    img = Image.open(img_input)
    st.image(img, use_container_width=True)
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Analizando..."):
            resultado = identificar_planta(img)
            st.markdown("### Resultado del Análisis:")
            st.info(resultado) # Usamos info para que resalte más el texto
