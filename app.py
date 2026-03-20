import streamlit as st
from google import genai
from PIL import Image

# 1. Configuración inicial
st.set_page_config(page_title="Flora - ID Botánico", layout="centered", page_icon="🌿")

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies vegetales.")

# 2. Inicialización del cliente
try:
    # Usa la API Key de tus Secrets de Streamlit
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Entrada de imagen
opcion = st.radio("Fuente:", ["📷 Cámara", "📁 Archivo"], horizontal=True)
archivo = st.camera_input("Capturar") if opcion == "📷 Cámara" else st.file_uploader("Sube imagen", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    if opcion == "📁 Archivo":
        st.image(img, use_container_width=True)

    if st.button("🔍 INICIAR IDENTIFICACIÓN"):
        with st.spinner('Procesando...'):
            try:
                prompt = (
                    "Actúa como un botánico experto. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye Maya), "
                    "distribución neotropical y estatus de conservación (NOM-059/UICN)."
                )

                # EL CAMBIO DEFINITIVO:
                # En cuentas de pago de Google Cloud, el modelo DEBE llevar el prefijo 'models/'
                # para que la librería lo encuentre correctamente.
                response = client.models.generate_content(
                    model="models/gemini-2.0-flash", 
                    contents=[prompt, img]
                )

                st.success("Análisis completado")
                st.markdown(f"### Resultado:\n{response.text}")

            except Exception as e:
                # Si el 2.0 falla por ser muy nuevo en tu región, intenta el 1.5 con el prefijo correcto
                if "404" in str(e) or "429" in str(e):
                    try:
                        response = client.models.generate_content(
                            model="models/gemini-1.5-flash",
                            contents=[prompt, img]
                        )
                        st.success("Análisis completado (Respaldo)")
                        st.markdown(response.text)
                    except Exception as e_final:
                        st.error(f"Error persistente de cuota o modelo: {e_final}")
                else:
                    st.error(f"Error técnico: {e}")

st.divider()
st.caption("Investigación Científica | Google Cloud")
