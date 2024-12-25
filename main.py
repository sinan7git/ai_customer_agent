from flask import Flask, request, Response
from flask_cors import CORS
from ai import get_ai_response, transcribe
from elevenlabs import generate, stream, set_api_key, voices
import key

app = Flask(__name__)
CORS(app)

set_api_key(key.ELEVENLABS_API_KEY)

@app.route("/speak", methods=["POST"])
def speak():
    try:
        question = transcribe(request)
        print("Transcribed question:", question)

        generate_response = get_ai_response(question)
        response_text = ''.join(generate_response())
        print("Generated AI response:", response_text)

        try:
            available_voices = [voice.name for voice in voices()]
        except Exception as e:
            print("Error fetching voices:", e)
            available_voices = []

        voice_name = "Sarah" if "Sarah" in available_voices else (available_voices[0] if available_voices else None)

        if not voice_name:
            return {"error": "No available voices found. Check your Eleven Labs API key or voice configuration."}, 500

        audio = generate(
            text=response_text,
            voice=voice_name,
            model="eleven_multilingual_v2",
            stream=True
        )
        return Response(audio, mimetype="audio/mpeg")

    except Exception as e:
        print("Error in /speak endpoint:", e)
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
