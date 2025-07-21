from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import os

app = Flask(__name__)

# Load the model once at startup
model = WhisperModel("base", compute_type="int8")  # Use "float16" if running on GPU

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

    # Collect the full text
    transcription = " ".join([segment.text for segment in segments])

    # Clean up the file
    os.remove(filepath)

    return jsonify({
        "language": info.language,
        "transcription": transcription
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
