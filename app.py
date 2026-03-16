def analizar_imagen_directo(img):
    try:
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Identifica esta planta de la Península de Yucatán. Responde el nombre científico y común. Si no puedes identificarla, explica por qué."},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }]
        }
        
        response = requests.post(URL, json=payload, headers=headers)
        res_json = response.json()
        
        # --- NUEVA VALIDACIÓN DE SEGURIDAD ---
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            texto_respuesta = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            return texto_respuesta
        elif 'error' in res_json:
            return f"Error de Google API: {res_json['error']['message']}"
        else:
            return "La IA no pudo generar un resultado para esta imagen. Intenta con una foto más clara o de más cerca."
        # -------------------------------------

    except Exception as e:
        return f"Error técnico: {str(e)}"
