import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Configuración de la página
st.set_page_config(page_title="Flora ID", layout="centered", page_icon="🌿")
st.title("🌿 Flora: Análisis Botánico")

# 1. Configuración de la API Key
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets.")
    st.stop()

archivo = st.camera_input("Capturar planta") or st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

if archivo:
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Procesando imagen...'):
            try:
                # Usamos el modelo 1.5 Flash, que es el más estable para visión
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(archivo)
                
                # Prompt estructurado para tu investigación en ECOSUR
                prompt = (
                    "Actúa como un botánico experto de la región Maya. Identifica esta planta y proporciona: "
                    "Nombre científico, familia, nombres comunes (incluye nombres en Maya), "
                    "hábitat y estatus de conservación según la NOM-059-SEMARNAT."
                )
                
                # Intentamos la generación estándar
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("Análisis completado")
                    st.markdown(response.text)
                else:
                    st.warning("No se recibió una respuesta clara. Intenta con otra foto.")
                
            except Exception as e:
                # Si el error 404 persiste, el problema está en la Key de Google Cloud
                st.error(f"Error de conexión: {e}")
                st.info("Asegúrate de que la API Key en Secrets sea la que generaste en la Consola de Google Cloud (no la de AI Studio).")
