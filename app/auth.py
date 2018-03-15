from functools import wraps
from datetime import datetime
from flask import request, abort

from .models import Token

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.form:
            token = request.form.get('token')
        elif request.json:
            token = request.json.get('token')
        else:
            abort(400)
        now = datetime.utcnow()
        token = Token.query.filter(Token.token==token).first()
        if not token or token.expires_at < now:
            abort(400)
        return f(*args, **kwargs)
    return wrapper