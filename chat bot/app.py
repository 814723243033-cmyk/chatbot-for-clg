from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from src.chatbot import chatbot

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    q = request.json.get("question", "")
    ans = chatbot(q)
    return jsonify({"answer": ans})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
