from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__) 

socketio= SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_msg(msg):
    print("Message: " + msg)
    send(msg, broadcast=True)

@socketio.on("connect")
def handle_connect():
    print("A client has connected")
    send("A new user has joined the chat", broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    print("A client has disconnected")
    send("A user has left the chat", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
