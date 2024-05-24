from functools import wraps
import jwt
from flask import jsonify, request, abort
from flask import current_app
from models.user import User
from werkzeug.exceptions import Unauthorized
from flask import current_app



#- TOKEN FUNCTION
#################
# JWT from https://www.youtube.com/watch?v=WxGBoY5iNXY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
     
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message' : 'Token fehlt!'}), 401

        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            current_user = current_app.cache.get(data['public_id'])
            if current_user is None:
                current_user = User.query.filter_by(public_id=
                                                    data['public_id']).first()
                current_app.cache.set(data['public_id'], current_user, timeout=60*60)
            
        except:
            abort(401, message='Token nicht (mehr) gültig!')
       

        return f(current_user, *args, **kwargs)

    return decorated
