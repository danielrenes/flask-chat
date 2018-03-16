from flask import Blueprint, render_template, request, abort, jsonify, current_app

from . import db
from .models import User, Message, Token
from .auth import token_required
from .notifications import push_users, push_messages

ui = Blueprint('ui', __name__)
usr = Blueprint('usr', __name__)
msg = Blueprint('msg', __name__)

@ui.route('/', methods=['GET'])
def index():
    active_users = User.query.filter(User.active==True).all()
    messages = Message.query.join(User, User.id==Message.user_id).all()
    return render_template('index.html', active_users=active_users, messages=messages)

@usr.route('/user/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if not username:
        abort(400)
    user = User.query.filter(User.name==username).first()
    if not user:
        abort(400)
    if user.active:
        return '', 304
    password = request.form.get('password')
    if user.password != password:
        abort(400)
    user.active = True
    token_data = user.generate_token()
    token = Token(token=token_data['token'], expires_at=token_data['expires_at'], user_id=user.id)
    db.session.add(token)
    db.session.commit()
    push_users()
    return jsonify({
        'token': token_data['token']
    })

@usr.route('/user/logout', methods=['POST'])
@token_required
def logout():
    user = User.query.join(Token, User.id==Token.user_id).filter(Token.token==request.json.get('token')).first()
    if not user:
        abort(400)
    if not user.active:
        abort(400)
    user.active = False
    db.session.commit()
    push_users()
    return '', 200

@usr.route('/user/token', methods=['POST'])
def renew_token():
    token = request.json.get('token')
    if not token:
        abort(400)
    old_token = Token.query.filter(Token.token==token).first()
    if not token:
        abort(400)
    user = User.query.join(Token, User.id==Token.user_id).filter(User.token==old_token).first()
    if not user:
        abort(400)
    db.session.delete(old_token)
    token_data = user.generate_token()
    new_token = Token(token=token_data['token'], expires_at=token_data['expires_at'], user_id=user.id)
    db.session.add(new_token)
    db.session.commit()
    return jsonify({
        'token': token_data['token']
    })

@msg.route('/msg/send', methods=['POST'])
@token_required
def send():
    text = request.form.get('text')
    if not text:
        abort(400)
    user = User.query.join(Token, User.id==Token.user_id).filter(Token.token==request.form.get('token')).first()
    if not user:
        abort(400)
    msg = Message(text=text, user_id=user.id)
    db.session.add(msg)
    db.session.commit()
    push_messages()
    return '', 200
