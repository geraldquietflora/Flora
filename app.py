import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# Configuración de la interfaz
st.set_page_config(page_title="Flora ID - Campo", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Identificación Botánica")
st.caption("Versión Optimizada para Trabajo en Campo (ECOSUR)")

# Verificación de API Key
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Entrada de imagen
st.write("### Captura o selecciona una muestra")
foto = st.camera_input("Tomar foto") or st.file_uploader("O subir archivo", type=["jpg", "png", "jpeg"])

if foto:
    if st.button("🔍 ANALIZAR ESPECIE"):
        with st.spinner('Procesando caracteres morfológicos...'):
            try:
                # 1. Preparación de imagen
                img = Image.open(foto)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # 2. Obtener lista de modelos y filtrar por cuota (FLASH SOLAMENTE)
                models_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
                models_resp = requests.get(models_url).json()
                
                # Buscamos modelos que soporten generación de contenido y que sean FLASH
                # Esto evita el Error 429 de los modelos Pro que tienen cuota 0 o muy baja
                available_flash_models = [
                    m['name'] for m in models_resp.get('models', []) 
                    if 'generateContent' in m.get('supportedGenerationMethods', []) 
                    and 'flash' in m['name'].lower()
                ]

                if not available_flash_models:
                    st.error("No se encontraron modelos Flash disponibles en tu cuenta.")
                    st.stop()

                # Seleccionamos el modelo más reciente (usualmente el primero o gemini-1.5-flash)
                selected_model = available_flash_models[0]

                # 3. Prompt especializado para rigor científico
                prompt_text = (
                    "Actúa como un botánico taxónomo experto en la Flora de la Península de Yucatán. "
                    "Analiza la imagen y responde con este rigor: \n"
                    "1. MORFOLOGÍA: Describe caracteres diagnósticos visibles (hojas, flores, tallo). \n"
                    "2. IDENTIFICACIÓN: Nombre científico (con autor), Familia y Nombres Comunes (énfasis en Maya). \n"
                    "3. DISTRIBUCIÓN: Confirma si es nativa o introducida en la Península de Yucatán. \n"
                    "4. NOM-059: Indica estatus de conservación si aplica. \n"
                    "Si la foto no es clara, indica qué carácter falta para una identificación segura."
                )

                # 4. Petición Directa (Evita el error 404)
                url = f"https://generativelanguage.googleapis.com/v1/{selected_model}:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": prompt_text},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_str}}
                        ]
                    }]
                }

                response = requests.post(url, json=payload)
                res_json = response.json()

                if response.status_code == 200:
                    resultado = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success(f"Analizado con {selected_model}")
                    st.markdown("---")
                    st.markdown(resultado)
                elif response.status_code == 429:
                    st.warning("⚠️ Cuota temporal agotada. Por favor, espera 10 segundos y presiona el botón de nuevo.")
                else:
                    st.error(f"Error {response.status_code}: {res_json.get('error', {}).get('message', 'Error desconocido')}")

            except Exception as e:
                st.error(f"Error técnico: {e}")

st.markdown("---")
st.info("Nota: Este motor prioriza modelos 'Flash' para garantizar disponibilidad en campo.")
