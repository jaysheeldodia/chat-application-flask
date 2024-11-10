from flask import Flask, render_template, request # type: ignore
from flask_socketio import SocketIO, send, emit # type: ignore

app = Flask(__name__) 

socketio = SocketIO(app)

active_users = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("send_msg")
def handle_send_msg(data):
    print(f"Username is {data['userName']}")
    print(f"userId is {data['userId']}")
    print(f"message is {data['message']}")
    message = {
        "userName": data['userName'],
        "message": data['message']
    }
    
    message = f"{data['userName']}: {data['message']}"
    
    print("the message is ")
    print(message)
    
    
    emit("incoming_msg", message, broadcast=True, include_self=False)
    # socketio.emit("incoming_msg", message, broadcast=True, include_self=True)

# @socketio.on("message")
# def handle_msg(msg):
#     if msg["type"] == "connection":
#         print("Connected user ", msg["data"])
#     elif msg["type"] == "msg":
#         print(f"{msg["userName"]}: " + msg["data"])
#         send(msg, broadcast=True)

@socketio.on("connected")
def handle_connect(data):
    uid = request.sid
    active_users[uid] = data['userName']
    msg = f"{data['userName']} has connected!"
    emit("connection_msg",  msg, broadcast=True, include_self=False)

@socketio.on("disconnect")
def handle_disconnect():
    uid = request.sid
    msg = f"{active_users[uid]} has disconnected!"
    del active_users[uid]
    emit("message", msg, broadcast=True, include_self=False)

    
if __name__ == "__main__":
    socketio.run(app, debug=True)
