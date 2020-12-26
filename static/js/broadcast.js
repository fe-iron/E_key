let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');
let only_once = true;
function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser || message.first_name === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.first_name}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getMessageById(message) {
    id = JSON.parse(message).message
<<<<<<< HEAD
    if(only_once){
        $.getJSON(`/api/v1/message/${id}/`, function (data) {
            if (data.user === currentRecipient[0] ||
                (data.recipient === currentRecipient[0] && data.user == currentUser)) {
                drawMessage(data);
            }
            messageList.animate({scrollTop: messageList.prop('scrollHeight')});

        });
    }
=======
    $.getJSON(`/api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient[0] ||
            (data.recipient === currentRecipient[0] && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});

    });
>>>>>>> 2ff158a61a5ee690761feb0066d0266705661809
}

function sendMessage(recipients, body) {
    only_once = true;
    $.post('/api/v1/message/', {
            recipient: JSON.stringify(recipients),
            body: body
        }).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    setCurrentRecipient(recipient);
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

    var socket = new WebSocket(
        ws_scheme+'://' + window.location.host +
        ':8001/'+ws_scheme+'?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
        only_once = false;
    };

});


function go_back() {
    window.history.back();
}
