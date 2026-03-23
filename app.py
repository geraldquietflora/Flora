import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico Especializado")

api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets.")
    st.stop()

st.write("### Captura o selecciona una imagen de muestra")
foto = st.camera_input("Tomar foto con la cámara") or st.file_uploader("O subir archivo", type=["jpg", "png", "jpeg"])

if foto:
    if st.button("🔍 IDENTIFICAR ESPECIE (ANÁLISIS BOTÁNICO)"):
        with st.spinner('Realizando análisis morfológico detallado...'):
            try:
                # Preparar imagen
                img = Image.open(foto)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # 1. AUTO-DETECCIÓN DE MODELO (Usamos lo que ya funciona)
                models_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
                models_resp = requests.get(models_url).json()
                
                # Buscamos el modelo más capaz (preferimos pro, luego flash)
                available_models = [m['name'] for m in models_resp.get('models', []) 
                                   if 'generateContent' in m.get('supportedGenerationMethods', [])]
                
                # Priorizar modelos Pro si están disponibles, si no Flash 2.5/1.5
                best_model = None
                for m_name in ['pro', 'flash-2.5', 'flash-1.5', 'flash']:
                    for avail in available_models:
                        if m_name in avail:
                            best_model = avail
                            break
                    if best_model: break
                
                if not best_model:
                    st.error("No se encontraron modelos compatibles.")
                    st.stop()
                
                # 2. PROMPT ESPECIALIZADO PARA PRECISIÓN CIENTÍFICA
                # Este prompt obliga al modelo a analizar caracteres diagnósticos
                prompt_text = (
                    "Actúa como un botánico taxónomo experto en la Flora de la Península de Yucatán (MEXU/ECOSUR). "
                    "Analiza esta imagen con extremo rigor botánico. Tu objetivo es la precisión, no la velocidad. "
                    "Por favor, sigue este protocolo de identificación: \n"
                    "1. ANALIZA LA MORFOLOGÍA VISIBLE: Describe caracteres diagnósticos clave (filotaxia, forma y margen foliar, presencia/tipo de pubescencia, caracteres florales o de fruto si son visibles). \n"
                    "2. IDENTIFICA LA ESPECIE: Proporciona el Nombre Científico, Autoría, Familia (con ortografía correcta, ej. Fabaceae, no Leguminosae) y Nombres Comunes (destacando el Maya y su contexto cultural si aplica). \n"
                    "3. VERIFICA CON FLORA LOCAL: Asegúrate de que la especie propuesta esté distribuida en la Península de Yucatán o el Caribe mexicano. \n"
                    "4. CONFIRMACIÓN Y DUDA: Si la identificación no es 100% segura debido a la calidad de imagen o falta de caracteres diagnósticos, indícalo claramente y sugiere qué caracteres faltan (ej. 'Requiere observación de estípulas'). \n"
                    "5. ESTATUS DE CONSERVACIÓN: Menciona su categoría en la NOM-059-SEMARNAT-2010 (P, A, Pr, Pr*, E) o si No Aplica."
                )

                # 3. PETICIÓN AL SERVIDOR
                url = f"https://generativelanguage.googleapis.com/v1/{best_model}:generateContent?key={api_key}"
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
                    st.success(f"Análisis completado con {best_model}")
                    st.markdown("---")
                    st.markdown(resultado)
                else:
                    st.error(f"Error {response.status_code}: {res_json}")

            except Exception as e:
                st.error(f"Error técnico: {e}")
