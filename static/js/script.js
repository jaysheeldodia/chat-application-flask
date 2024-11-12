const socket = io();

const inputElement = document.getElementById("message");

let userId = null;
let userName = null;

// add message to the chatbox
const addMsgToChatBox = (messageToAdd) => {
    const chatBox = document.getElementById('chat-box');
    const p = document.createElement('p');
    p.innerText = messageToAdd;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the bottom
}

// socket.on("connect", function() {
//     socket.emit("connected", {
//         "userName": userName,
//     })
// })

socket.on("disconnect", function() {
    socket.emit("disconnected", {
        "userName": userName,
    })
})

socket.on("message", function(data) {
    addMsgToChatBox(data)
})

socket.on("incoming_msg", function(data) {
    addMsgToChatBox(data)
})

socket.on("self_connection_data", function(data) {
    userName = data['userName']
    console.log(userName);
})

socket.on("connection_msg", function(data) {
    addMsgToChatBox(data['message']);
})

socket.on("disconnection_msg", function(data) {
    console.log("This message is called")
    addMsgToChatBox(data);
})

// Function to send message
function sendMessage() {
    console.log("Send msg function");
}

document.getElementById('message').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const message = document.getElementById('message').value;
    if (message) {
        let data = {
            "userName": userName,
            "userId": socket.id,
            "message": message,
            "messageType": "incoming_msg",
        }
        console.log("sending socket data")
        console.log(data)
        socket.emit('send_msg', data)
        self_msg = "You: " + message;
        addMsgToChatBox(self_msg);
        // Send the message to the server
        document.getElementById('message').value = '';  // Clear the input
    }
}

// Event listener for incoming messages
// socket.on('incoming_message', function (msg) {
//     const chatBox = document.getElementById('chat-box');
//     const p = document.createElement('p');
//     p.innerText = msg["data"];
//     chatBox.appendChild(p);
//     chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the bottom
// });