from flask import Flask, request, jsonify, render_template
import cohere
import os
import whisper
import tempfile
from flask_cors import CORS
from dotenv import load_dotenv

# Add ffmpeg to path
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-7.1.1-full_build\bin"

# Load env vars
load_dotenv()

# Init Flask app
app = Flask(__name__)
CORS(app)

# Set Cohere API key
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Load Whisper model once at startup
model = whisper.load_model("base")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"answer": "No question provided."}), 400

        response = co.chat(
            message=question,
            model="command-r"
        )

        return jsonify({"answer": response.text})

    except Exception as e:
        print("Error:", e)
        return jsonify({"answer": "There was an error calling Cohere. Check the server logs."}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio_file.save(temp_audio.name)
        temp_audio_path = temp_audio.name  # Save path for later use

    # Transcribe after file is closed
    result = model.transcribe(temp_audio_path)

    # Clean up safely
    try:
        os.unlink(temp_audio_path)
    except Exception as e:
        print(f"Warning: Failed to delete temp file: {e}")

    return jsonify({"transcription": result["text"]})

if __name__ == "__main__":
    app.run(debug=True)
