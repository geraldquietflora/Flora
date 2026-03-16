import streamlit as st
import requests

st.set_page_config(page_title="Diagnóstico Flora", page_icon="🔧")

API_KEY = st.secrets["GOOGLE_API_KEY"]

st.title("🔧 Diagnóstico de Modelos")
st.write("Consultando la lista de modelos permitidos para tu API KEY...")

if st.button("🔍 LISTAR MODELOS DISPONIBLES"):
    try:
        # Consultamos la lista oficial de modelos de tu cuenta
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
        response = requests.get(url)
        res_json = response.json()
        
        if 'models' in res_json:
            st.success("¡Conexión exitosa! Estos son los modelos que puedes usar:")
            for m in res_json['models']:
                # Solo mostramos los que sirven para generar contenido
                if 'generateContent' in m['supportedGenerationMethods']:
                    st.code(m['name'])
        else:
            st.error(f"Error al listar: {res_json}")
    except Exception as e:
        st.error(f"Error técnico: {e}")

st.divider()
st.info("Copia los nombres que aparezcan arriba para que podamos ajustar la app.")
