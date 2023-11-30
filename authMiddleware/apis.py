from functools import wraps
from flask import abort, request
import jwt


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')

            if auth_header is None:
                abort(401)

            token = auth_header.split(" ")[1]

            try:
                decoded_token = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
                if 'role' not in decoded_token or decoded_token['role'] != required_role:
                    abort(403)

                kwargs['user'] = decoded_token

                return func(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                abort(401) 
            except jwt.InvalidTokenError:
                abort(401)

        return wrapper
    return decorator