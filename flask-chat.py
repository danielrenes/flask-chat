#!/usr/bin/env python

from app import create_app, db, socketio

app = create_app()

@app.cli.command('init-db', help='Create a fresh database.')
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

@app.cli.command('debug', help='Start in debug mode.')
def debug():
    db.drop_all()
    db.create_all()

    from app.models import User

    fake_users = [
		{'name': 'Alice', 'password': 'alice'},
		{'name': 'Bob', 'password': 'bob'},
		{'name': 'Caesar', 'password': 'caesar'}
	]

    for fake_user in fake_users:
        user = User()
        user.name = fake_user['name']
        user.password = fake_user['password']
        db.session.add(user)
        db.session.commit()

    socketio.run(app, debug=True, port=10000)
