from flask import Flask, request, jsonify
from flask_cors import CORS
from main import SIRIRAJ

app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

siriraj = SIRIRAJ()
siriraj.start()  # Start background thread for task processing

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    siriraj.process_query(message)
    # Wait for a response to appear in queue
    timeout = 10
    start = time.time()
    while time.time() - start < timeout:
        if not response_queue.empty():
            return jsonify({"reply": response_queue.get()})
        time.sleep(0.1)
    return jsonify({"reply": "No response from AI."})

@app.route("/toggle_mic", methods=["POST"])
def toggle_mic():
    data = request.get_json()
    siriraj.mic_on = data.get("mic", True)
    return jsonify({"status": "Mic updated"})

@app.route("/toggle_speaker", methods=["POST"])
def toggle_speaker():
    data = request.get_json()
    siriraj.speaker_on = data.get("speaker", True)
    return jsonify({"status": "Speaker updated"})

if __name__ == "__main__":
    app.run(debug=True)
