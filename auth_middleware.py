from functools import wraps
import jwt
from flask import jsonify, request, abort
from flask import current_app
from models.user import User

#- TOKEN FUNCTION
#################
# JWT from https://www.youtube.com/watch?v=WxGBoY5iNXY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token fehlt!'}), 401

        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            current_user = User.query.filter_by(public_id=
                                                data['public_id']).first()
        except:
            abort(401, message='Token nicht (mehr) gültig!')
       

        return f(current_user, *args, **kwargs)

    return decorated
