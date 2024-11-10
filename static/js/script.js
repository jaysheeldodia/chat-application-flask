const socket = io();
const userName = window.prompt("Enter your name ");
socket.send(({
    "data": userName,   
    "type": "connection"
}))

const inputElement = document.getElementById("message");


let userId = null;

// add message to the chatbox
const addMsgToChatBox = (messageToAdd) => {
    const chatBox = document.getElementById('chat-box');
    const p = document.createElement('p');
    p.innerText = messageToAdd;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the bottom
}



socket.on("message", function(data) {
    addMsgToChatBox(data)
})

socket.on("connection_msg", function(data) {
    addMsgToChatBox(data);
})

socket.on("disconnection_msg", function(data) {
    console.log("This message is called")
    addMsgToChatBox(data);
})

socket.on("connect", function() {
   
    socket.emit("connected", {
        "userName": userName,
    })
})

socket.on("disconnect", function() {
    socket.emit("disconnected", {
        "userName": userName,
    })
})


// Function to send message
function sendMessage() {
    console.log("Send msg function");
}


// // Function to send message
// function sendMessage() {
//     const message = document.getElementById('message').value;
//     if (message) {
//         data = {
//             "type": "incoming_msg",
//             "userName": userName,
//             "message": message
//         }
//         console.log("sending socket data")
//         socket.emit('send_msg', data)
//         // Send the message to the server
//         document.getElementById('message').value = '';  // Clear the input
//     }
// }



// Event listener for incoming messages
socket.on('incoming_message', function (msg) {
    const chatBox = document.getElementById('chat-box');
    const p = document.createElement('p');
    p.innerText = msg["data"];
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the bottom
});