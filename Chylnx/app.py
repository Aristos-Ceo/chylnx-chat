
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)  # REMOVED template_folder parameter
app.config['SECRET_KEY'] = "secret123"
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    print("🔗 User connected")
    emit("connected", {"status": "success"})

@socketio.on("message")
def handle_message(data):
    print("📨 Message received:", data)
    message_text = data.get("text", "").strip()
    if message_text:
        emit("new_message", {
             "username": data.get("username", "User"),
            "message": message_text,
            "timestamp": datetime.now().isoformat()
        }, broadcast=True)

if __name__ == "__main__":
    print("🚀 Starting chat server...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)