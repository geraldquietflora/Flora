import streamlit as st
from google import genai
from PIL import Image

# 1. Configuración de página (Indispensable al inicio)
st.set_page_config(page_title="Flora - ID Botánico", layout="centered", page_icon="🌿")

st.markdown("<style>.stButton>button {width:100%; background-color: #2e7d32; color: white; font-weight: bold; height: 3em; border-radius: 10px;}</style>", unsafe_allow_html=True)

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies vegetales.")

# 2. Inicialización del cliente
try:
    # Lee la llave desde Settings > Secrets en Streamlit Cloud
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("⚠️ Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Entrada de imagen
opcion = st.radio("Fuente:", ["📷 Cámara", "📁 Archivo"], horizontal=True)
archivo = st.camera_input("Capturar") if opcion == "📷 Cámara" else st.file_uploader("Sube imagen", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    if opcion == "📁 Archivo":
        st.image(img, use_container_width=True)

    if st.button("🔍 INICIAR IDENTIFICACIÓN"):
        with st.spinner('Conectando con Google Cloud...'):
            try:
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye Maya), "
                    "distribución neotropical y estatus de conservación (NOM-059/UICN)."
                )

                # USAMOS EL NOMBRE TÉCNICO COMPLETO PARA EVITAR EL ERROR 404
                # Este nombre es el estándar para cuentas de pago en Google Cloud
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=[prompt, img]
                )

                st.success("Análisis completado")
                st.markdown(f"### Resultado:\n{response.text}")

            except Exception as e:
                if "429" in str(e):
                    st.warning("⏳ Límite de cuota alcanzado. Google Cloud está procesando la validación de tu tarjeta. Intenta en unos minutos.")
                elif "404" in str(e):
                    # Si el 1.5 falla, intentamos el 2.0 con el nombre técnico
                    try:
                        response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, img])
                        st.success("Análisis completado (Modelo 2.0)")
                        st.markdown(response.text)
                    except:
                        st.error("Error: El modelo no responde. Verifica que la API de Gemini esté habilitada en tu consola de Google Cloud.")
                else:
                    st.error(f"Detalle del error: {e}")

st.divider()
st.caption("Unidad de Apoyo a la Investigación | Facturación Activa")
