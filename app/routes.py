from flask import Blueprint, render_template, session
from flask_socketio import emit, join_room, leave_room
from app import socketio, db
from app.models import User, Message
from datetime import datetime

bp = Blueprint('main', __name__)

online_users = []

@bp.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    if username not in online_users:
        online_users.append(username)
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    emit('message', {'username': 'System', 'message': f'{username} has joined the chat.', 'timestamp': datetime.now().isoformat()}, broadcast=True)
    emit('update_users', online_users, broadcast=True)
    
    # Send last few messages to the new user
    last_messages = Message.query.order_by(Message.id.desc()).limit(10).all()
    messages_data = [{'username': msg.username, 'message': msg.message, 'timestamp': msg.timestamp.isoformat()} for msg in reversed(last_messages)]
    emit('last_messages', messages_data)

@socketio.on('message')
def handle_message(data):
    message = Message(username=data['username'], message=data['message'], timestamp=datetime.now())
    db.session.add(message)
    db.session.commit()
    data['timestamp'] = message.timestamp.isoformat()
    emit('message', data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in online_users:
        online_users.remove(username)
        emit('message', {'username': 'System', 'message': f'{username} has left the chat.', 'timestamp': datetime.now().isoformat()}, broadcast=True)
        emit('update_users', online_users, broadcast=True)
