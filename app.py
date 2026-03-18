import streamlit as st
from google import genai
from PIL import Image
import time

# 1. Configuración de página
st.set_page_config(page_title="Flora - ID Botánico", layout="centered", page_icon="🌿")

# Estilo para el botón
st.markdown("<style>.stButton>button {width:100%; background-color: #2e7d32; color: white; font-weight: bold; height: 3em; border-radius: 10px;}</style>", unsafe_allow_html=True)

st.title("🌿 Flora: Análisis Botánico")
st.write("Identificación científica de especies vegetales.")

# 2. Inicialización del cliente con Secrets
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("⚠️ Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit Cloud.")
    st.stop()

# 3. Entrada de imagen
opcion = st.radio("Fuente:", ["📷 Cámara", "📁 Archivo"], horizontal=True)
archivo = st.camera_input("Capturar") if opcion == "📷 Cámara" else st.file_uploader("Sube imagen", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    if opcion == "📁 Archivo":
        st.image(img, use_container_width=True)

    if st.button("🔍 INICIAR IDENTIFICACIÓN"):
        with st.spinner('Analizando con IA de alta precisión...'):
            # Definimos el prompt científico una sola vez
            prompt = (
                "Identifica esta planta. Proporciona: Nombre científico, familia, "
                "nombres comunes (incluye nombres en Maya si es de la región), "
                "distribución y estatus de conservación (NOM-059/UICN)."
            )
            
            # Lógica de respaldo (Failover): Intentar 2.0, si falla, intentar 1.5
            modelos_a_probar = ["gemini-2.0-flash", "gemini-1.5-flash"]
            exito = False
            
            for nombre_modelo in modelos_a_probar:
                try:
                    response = client.models.generate_content(
                        model=nombre_modelo,
                        contents=[prompt, img]
                    )
                    st.success(f"Análisis completado (Modelo: {nombre_modelo})")
                    st.markdown(f"### Resultado:\n{response.text}")
                    exito = True
                    break # Si funciona, salimos del bucle
                except Exception as e:
                    if "429" in str(e):
                        continue # Si es error de cuota, probamos el siguiente modelo
                    else:
                        st.error(f"Error con {nombre_modelo}: {e}")
                        break
            
            if not exito:
                st.warning("⚠️ Google Cloud aún limita tu cuota. Esto sucede durante las primeras 24-48h de activar una tarjeta. Por favor, reintenta en unos minutos.")

st.divider()
st.caption("Investigación y Desarrollo | Google Cloud Pay-as-you-go")
