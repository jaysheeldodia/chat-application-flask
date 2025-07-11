# Real Time Chat Application

## Author : Jaysheel Dodia

## Features: 

Common argument name on server side and client side: data

<!-- * [x] -->
* [x] On connection - 
    - Connnection message to all
    - Broadcast message to all that this person has connected except for the sender

* [x] On Disconnect - 
    - Disconnect message to all
    - Broadcast message to all that this person has disconnected except for the sender
    
* [x] On message send
    1. JS Side Send - function send_msg
    2. Server side receive
    3. Server side Broadcast (Self Include = False)
    4. JS Side receive - function incoming_msg
    - Emit message to server 
        -> userName
        -> userId (socketid)
        -> message
        -> messageType
    - Server emit message to the client
        -> Send the userName
        -> send the message

* [x] Temporary dictionary database
    - use the socket id, name, password and other things to store into the dictionary for now
    

* [x] Implement the login

* [ ] Setup db using SQLITE3

* [ ] Better user name input
    - UI for the same

* [ ] Rooms

* [ ] Rooms with passwords

* [ ] Channels for admins

* [ ] Work on the UI

* [ ] Deobfuscate

* [ ] Next word prediction
