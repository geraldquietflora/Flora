import google.generativeai as genai
import os

# 1. CONFIGURACIÓN DE SEGURIDAD
# Sustituye el texto entre comillas por tu clave real de Google AI Studio
API_KEY = "AIzaSyA12GiqlG50X_kT6iPBIXGGnq1pGuFXXl0"

try:
    genai.configure(api_key=API_KEY)
    
    # 2. SELECCIÓN DEL MODELO
    # Usamos 'gemini-1.5-flash' que es el estándar actual. 
    # Si este falla, el bloque 'except' nos dirá por qué.
    model_name = 'gemini-1.5-flash' 
    model = genai.GenerativeModel(model_name)

    # 3. FUNCIÓN PRINCIPAL DE PRUEBA
    def generar_respuesta(promp_usuario):
        try:
            print(f"--- Enviando pregunta a {model_name}... ---")
            response = model.generate_content(promp_usuario)
            return response.text
        except Exception as e:
            return f"Error al generar contenido: {str(e)}"

    # 4. EJECUCIÓN (Aquí es donde ocurre la magia)
    if __name__ == "__main__":
        print("SISTEMA INICIADO")
        pregunta = "Hola, ¿estás configurado correctamente? Responde brevemente."
        
        resultado = generar_respuesta(pregunta)
        
        print("\nRESPUESTA DEL MODELO:")
        print("-" * 30)
        print(resultado)
        print("-" * 30)

except Exception as e:
    print(f"ERROR CRÍTICO DE CONFIGURACIÓN: {e}")
