from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import os

app = Flask(__name__)

# Use a lighter model to avoid memory issues on free Render
model = WhisperModel("tiny", compute_type="int8")

@app.route('/')
def home():
    return "AI Study Buddy - Speech Transcription Ready"

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file temporarily
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # Transcribe audio
    segments, info = model.transcribe(filepath)
    transcription = " ".join([segment.text for segment in segments])

    # Clean up
    os.remove(filepath)

    return jsonify({
        "language": info.language,
        "transcription": transcription
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
