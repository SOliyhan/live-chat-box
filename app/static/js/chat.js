let socket;
let username;

function login() {
  username = document.getElementById('username').value;
  if (username) {
    document.getElementById('login').classList.add('d-none');
    document.getElementById('chatroom').classList.remove('d-none');
    socket = io.connect('http://localhost:5000');
    socket.emit('join', { username: username });

    socket.on('message', function(data) {
      let messages = document.getElementById('messages');
      let message = document.createElement('div');
      let timestamp = new Date(data.timestamp).toLocaleTimeString();
      message.innerHTML = `<strong>${data.username}:</strong> ${data.message} <small>${timestamp}</small>`;
      messages.appendChild(message);
      messages.scrollTop = messages.scrollHeight;
    });

    socket.on('update_users', function(users) {
      let usersList = document.getElementById('users');
      usersList.innerHTML = '';
      users.forEach(function(user) {
        let userItem = document.createElement('li');
        userItem.className = 'list-group-item';
        userItem.textContent = user;
        usersList.appendChild(userItem);
      });
    });

    socket.on('last_messages', function(messages) {
      let messagesDiv = document.getElementById('messages');
      messagesDiv.innerHTML = '';
      messages.forEach(function(data) {
        let message = document.createElement('div');
        let timestamp = new Date(data.timestamp).toLocaleTimeString();
        message.innerHTML = `<strong>${data.username}:</strong> ${data.message} <small>${timestamp}</small>`;
        messagesDiv.appendChild(message);
      });
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
  }
}

function sendMessage() {
  let message = document.getElementById('message').value;
  if (message) {
    socket.emit('message', { username: username, message: message });
    document.getElementById('message').value = '';
  }
}
