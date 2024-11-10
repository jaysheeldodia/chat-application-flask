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
    
* [ ] On message send
    - Emit message to server 
        -> userName
        -> userId
        -> message
        -> messageType
    - Server emit message to the client
        -> Send the userName
        -> send the message
        
* [ ] On message receive
    - Print the message in the format:
        -> userName: message