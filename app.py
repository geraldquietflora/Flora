import streamlit as st
import google.generativeai as genai  # <--- ESTA ES LA LÍNEA QUE FALTA
from PIL import Image
import io
import base64
import requests

# Configuración con los Secrets de Streamlit
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def analizar_imagen_directo(imagen_pil):
    # Optimizamos la imagen para la red de ECOSUR
    imagen_pil.thumbnail((1000, 1000))
    buf = io.BytesIO()
    imagen_pil.save(buf, format='JPEG', quality=85)
    img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": "Identifica el nombre científico de esta planta de la Península de Yucatán. Responde únicamente el nombre científico."},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
            ]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        res_json = response.json()
        return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
    else:
        return f"Error {response.status_code}: {response.text}"

# ==========================================
# 2. INTERFAZ DE USUARIO
# ==========================================
st.set_page_config(page_title="Flora Yucatán IA", page_icon="🌿")
st.title("🌿 Identificador de Flora (Versión 3.1)")
st.write("Unidad Chetumal - ECOSUR")

archivo = st.file_uploader("📂 Subir foto de campo", type=['jpg', 'png', 'jpeg'])
foto_camara = st.camera_input("📸 Tomar foto ahora")

foto = archivo if archivo else foto_camara

if foto:
    img = Image.open(foto)
    st.image(img, width=400, caption="Muestra a analizar")
    
    if st.button("🔍 IDENTIFICAR ESPECIE"):
        with st.spinner("Procesando con Gemini 3.1..."):
            nombre_ia = analizar_imagen_directo(img)
            
            if "Error" in nombre_ia:
                st.error(f"Fallo técnico: {nombre_ia}")
            else:
                st.success(f"**Identificación:** {nombre_ia}")
                
                # Cruce con tu base de datos local
                if os.path.exists('flora_yucatan.json'):
                    try:
                        with open('flora_yucatan.json', 'r', encoding='utf-8') as f:
                            datos = json.load(f)
                        encontrada = False
                        for p in datos:
                            if p["nombre_cientifico"].lower() in nombre_ia.lower() or nombre_ia.lower() in p["nombre_cientifico"].lower():
                                st.info(f"📍 **Datos Locales Encontrados:**\n\n* **Maya:** {p.get('nombre_maya')}\n* **NOM-059:** {p.get('estatus_nom059')}")
                                encontrada = True
                                break
                        if not encontrada:
                            st.warning("La especie no está en tu catálogo local .json")
                    except:
                        st.error("Error al leer flora_yucatan.json")

st.divider()
st.caption("Investigación ECOSUR 2026")
