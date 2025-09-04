import json
import base64
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Advertencia: No se encontró la clave GEMINI_API_KEY. El modo de desarrollo sin API estará disponible.")
    
try:
    if API_KEY:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error al configurar la API de Gemini: {e}")
    model = None

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("Advertencia: No se encontró la cadena de conexión MONGO_URI. Las funciones de base de datos no estarán disponibles.")
    client = None
else:
    try:
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Conexión a MongoDB exitosa!")
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        client = None

if client:
    db = client.language_tutor
    conversations_collection = db.conversations
else:
    conversations_collection = None


@app.route('/api/chat', methods=['POST'])
def chat():
    """Maneja las solicitudes de chat enviadas por el frontend."""
    if not model:
        return jsonify({"error": "El modelo de IA no está disponible en este momento."}), 503
        
    data = request.json
    prompt = data.get("prompt")
    history = data.get("history", [])

    if not prompt:
        return jsonify({"error": "No se proporcionó un mensaje."}), 400

    try:
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type='application/json'
            )
        )
        try:
            parsed_json = json.loads(response.text)
            return jsonify({"message": parsed_json})
        except json.JSONDecodeError:
            print("Error: El modelo no devolvió un JSON válido.")
            return jsonify({"error": "El servidor no pudo procesar la respuesta de la IA. Inténtalo de nuevo."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze_text', methods=['POST'])
def analyze_text():
    """
    Recibe texto del frontend, lo envía a la API de Gemini
    y devuelve el feedback de la IA.
    """
    if not model:
        return jsonify({"error": "El modelo de IA no está disponible. Por favor, asegúrate de que tu clave de API sea válida."}), 503

    try:
        data = request.json
        sentence = data.get('sentence')
        language = data.get('language')
        
        if not sentence:
            return jsonify({"error": "No se proporcionó texto para analizar."}), 400

        if language == 'es':
            prompt = f"""Eres un tutor de escritura profesional. Analiza la siguiente frase que te proporciono. Proporciona feedback sobre gramática, claridad y estilo, y posibles alternativas para mejorarla. No menciones el idioma en el que está escrita la frase ni la traduzcas. Responde de forma amigable y concisa, en español, en no más de dos párrafos.

Frase: "{sentence}"
"""
        else:
            prompt = f"""You are a professional writing tutor. Analyze the following sentence. Provide feedback on grammar, clarity, and style. For a business or formal context, suggest more specific, quoted alternative phrases. For a casual context, suggest more idiomatic or colloquial, quoted alternative phrases. Do not mention the original language of the sentence or translate it. Respond in a friendly and concise manner, in English, in no more than two paragraphs.

Sentence: "{sentence}"
"""
        response = model.generate_content(prompt)
        generated_text = response.text

        return jsonify({"feedback": generated_text})

    except Exception as e:
        print(f"Error inesperado al analizar el texto: {e}")
        return jsonify({"error": "Error interno del servidor. Por favor, inténtalo de nuevo."}), 500


@app.route('/api/save_conversation', methods=['POST'])
def save_conversation():
    """Guarda el historial completo de una conversación en la base de datos."""
    if not conversations_collection:
        return jsonify({"error": "La base de datos no está disponible."}), 503

    try:
        data = request.json
        conversation_data = {
            "user_id": data.get("user_id"),
            "history": data.get("history"),
            "timestamp": data.get("timestamp")
        }
        
        result = conversations_collection.insert_one(conversation_data)
        
        return jsonify({"message": "Conversación guardada con éxito", "id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-audio', methods=['POST'])
def analyze_audio():
    """Analiza la pronunciación del audio y lo devuelve en JSON."""
    if not model:
        return jsonify({"error": "El modelo de IA no está disponible. Por favor, asegúrate de que tu clave de API sea válida."}), 503
        
    data = request.json
    base64_audio = data.get("base64Audio")
    language = data.get("language")

    if not base64_audio:
        return jsonify({"error": "No se proporcionó audio."}), 400

    if language == 'es':
        prompt_text = (
            "Eres un tutor de pronunciación profesional. Analiza el audio del usuario. "
            "Proporciona una transcripción del audio y un análisis de pronunciación. "
            "La respuesta debe ser un objeto JSON con dos claves: 'transcribedText' (la transcripción) y 'wordFeedback' (un array de objetos para cada palabra). "
            "Cada objeto en el array 'wordFeedback' debe tener estas claves: 'word' (la palabra), 'correctlyPronounced' (booleano: true o false) y 'feedback' (un string detallado para esa palabra). "
            "Proporciona feedback específico y detallado para cada palabra. Sé constructivo."
        )
    else:
        prompt_text = (
            "You are a professional pronunciation tutor. Analyze the user's audio. "
            "Provide a transcription of the audio and a pronunciation analysis. "
            "The response should be a JSON object with two keys: 'transcribedText' (the transcription) and 'wordFeedback' (an array of objects for each word). "
            "Each object in the 'wordFeedback' array should have these keys: 'word' (the word), 'correctlyPronounced' (boolean: true o false), and 'feedback' (a detailed string for that word). "
            "Provide specific and detailed feedback for each word. Be constructive."
        )

    try:
        audio_data = base64.b64decode(base64_audio)
        
        response = model.generate_content(
            [
                prompt_text,
                {
                    "mime_type": "audio/webm",
                    "data": audio_data
                }
            ],
            generation_config=genai.GenerationConfig(
                response_mime_type='application/json'
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        try:
            result = json.loads(response.text)
            transcribed_text = result.get("transcribedText")
            word_feedback = result.get("wordFeedback")

            if not transcribed_text or not isinstance(word_feedback, list):
                return jsonify({"error": "La respuesta de la IA no tiene el formato esperado."}), 500

            return jsonify({
                "transcribedText": transcribed_text,
                "wordFeedback": word_feedback
            })

        except json.JSONDecodeError:
            print(f"La respuesta de la IA no es un JSON válido: {response.text}")
            return jsonify({"error": "Respuesta inválida del servidor de IA. Por favor, inténtalo de nuevo."}), 500

    except Exception as e:
        print(f"Error al analizar el audio: {e}")
        return jsonify({"error": f"Error del servidor al analizar el audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
