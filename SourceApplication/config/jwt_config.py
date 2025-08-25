import functools
import jwt # type: ignore
from flask import request, jsonify, current_app
# from config.db import get_db_connection

SECRET_KEY = '5367566B59703373367639792F423F4528482B4D6251655468576D5A71347437'

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            username = data.get('user') 
            
            if not username:
                return jsonify({'message': 'Username not found in token'}), 401
            
            # conn = get_db_connection()
            # cursor = conn.cursor()
            # cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
            # user_exists = cursor.fetchone()
            # conn.close()
            
            # if not user_exists:
            #     raise Exception('Invalid token') 
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(username, *args, **kwargs)

    return decorated