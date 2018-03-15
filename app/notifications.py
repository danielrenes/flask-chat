from . import socketio
from .models import User, Message

@socketio.on('connect', namespace='/notification')
def connect():
    print 'socketio client connected'

def push_users():
    active_users = [{'user': user.name} for user in User.query.filter(User.active==True).all()]
    socketio.emit('push_users', {'data': active_users}, namespace='/notification', broadcast=True)

def push_messages():
    messages = [{'text': message.text, 'user': message.user.name} for message in Message.query.join(User, User.id==Message.user_id).all()]
    socketio.emit('push_messages', {'data': messages}, namespace='/notification', broadcast=True)
