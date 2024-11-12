from flask import Flask, render_template, request, redirect, session, url_for # type: ignore
from flask_socketio import SocketIO, send, emit # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import logging

app = Flask(__name__) 
app.secret_key = os.urandom(24)
socketio = SocketIO(app, logger=False, engineio_logger=False)

# format
# dictionary
# login ? active_users[socketid] = username, name, email
# signup ? database_dictionary[username] = {name, email, password}

database_dictionary = {
    'testuser': generate_password_hash('password123'),
    'testuser2': generate_password_hash('password123'),
    'hello': generate_password_hash('password123'),
}
active_users = {}

# Route for index page "/"
@app.route("/")
def index():
    # if the username is present, session exists, no need to login again
    if 'username' not in session:
        return redirect(url_for('login'))
    # return index page if the user is logged in
    return render_template("index.html")

# route to login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    # if the session is present, redirect to index
    if 'username' in session:
        return redirect(url_for('index'))

    # else if the request method is 'POST', process the login
    if request.method == 'POST':

        # extract form data
        username = request.form['username']
        password = request.form['password']

        # if username in dictionary and if password is same as present in the database then login
        if username in database_dictionary and check_password_hash(database_dictionary[username], password):
                # set session username if the user is correct
                session['username'] = username

                # redirect to index page after login
                return redirect(url_for('index'))
                
        
        # if the username and password do not match, return failure
        return "The username and password does not match.Try again", 400 
    
    return render_template("login.html")

# Redirect to logout
@app.route("/logout")
def logout():
    # remove the usersession from the browser
    session.pop('username', None)

    # redirect to login page after the redirect
    return redirect(url_for("login"))

# Sign up page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if get request then return the signup page 
    if request.method == 'GET':
        return render_template("signup.html")

    # process the signup request if it is there
    else:
        print("Signup form request received")
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if username not in database_dictionary:
            database_dictionary[username] = { # type: ignore
                "name": name,
                "username": username,
                "email": email,
                "password": password
            }
        else:
            return "The username is already in use" 
        return redirect("/")

# Execute the script when the user connects
@socketio.on("connect")
def connect():
    uid = request.sid
    # add the user to the pool of active users
    active_users[uid] = database_dictionary[session['username']]

    # create a msg "user has connected!"
    msg = f"{session['username']} has connected!"
    # print('-'*50)
    # print(active_users)
    data = {
        "message": msg,
        "userName": session['username']
    }
    # send connection data to everyone except self
    emit("connection_msg",  data, broadcast=True, include_self=True)

    # send userName and other data to self
    emit("self_connection_data", data, broadcast=False)

# What happens when the user disconnects
@socketio.on("disconnect")
def disconnect():
    uid = request.sid

    # return msg that the user has disconnected
    msg = f"{session['username']} has disconnected!"
    # print(msg)
    # 
    # remoe the user from the active pool of users
    del active_users[uid]

    # emit the msg to everyone that the user has disconnected
    emit("message", msg, broadcast=True, include_self=False)

# Handle teh msg sent by the user
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

if __name__ == "__main__":
    # Disable Flask's default logger
    flask_log = logging.getLogger('werkzeug')
    flask_log.setLevel(logging.ERROR)  # Only log errors and above

    # Disable logging for SocketIO and Engine.IO
    socketio_log = logging.getLogger('socketio')
    socketio_log.setLevel(logging.ERROR)

    engineio_log = logging.getLogger('engineio')
    engineio_log.setLevel(logging.ERROR)
    socketio.run(app, debug=True)
