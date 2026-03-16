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
                    {"text": "Actúa como un botánico experto en la flora de la Península de Yucatán. Describe brevemente qué planta ves y proporciona su nombre científico y común. Si la imagen no es clara, da tu mejor estimación basada en las características visibles."},
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
        
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return "La IA recibió la imagen pero no pudo generar una descripción. Prueba con una foto más nítida."

    except Exception as e:
        return f"Error técnico: {str(e)}"
