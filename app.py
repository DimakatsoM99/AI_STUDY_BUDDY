from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    # Dummy response for now — replace with your AI logic
    return jsonify({"answer": f"You asked: {question}"})

@app.route('/transcribe', methods=['POST'])
def transcribe():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400
    
    # Dummy transcription — replace with real transcription code
    return jsonify({"transcription": "This is a sample transcription."})

if __name__ == '__main__':
    app.run(debug=True)
