import datetime
from flask import request, jsonify, make_response
# import bcrypt
from config.db import get_db_connection
from config.jwt_config import SECRET_KEY
import jwt # type: ignore

def signup():
    data = request.json
    
    name = data.get("fullname")
    username = data.get("username") 
    email = data.get("email")
    password = data.get("password")
    
    if not name or not username or not email or not password:
        return jsonify({"message": "All fields are required!"}), 400
    
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}'")
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        if existing_user[2] == username:
            return jsonify({"message": "Username already exists!"}), 409
        elif existing_user[3] == email:
            return jsonify({"message": "Email already exists!"}), 409
        
    # hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        cursor.execute(
            f"INSERT INTO users (name, username, email, password) VALUES ('{name}', '{username}', '{email}', '{password}')"
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"message": "Error inserting user into database.", "error": str(e)}), 500
    

    conn.close()
    return jsonify({"message": "Account created successfully!"}), 201

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400  
    
    conn = get_db_connection()
    cursor = conn.cursor()  
    
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    

    cursor.execute(f"SELECT username FROM users WHERE username = '{username}' AND password = '{password}'") 
    user = cursor.fetchone()
    
    conn.close()
    

    if user:
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1440)
        token = jwt.encode({
            'user': username,
            'exp': expiration_time,
        }, SECRET_KEY, algorithm='HS256')

        response = make_response(jsonify({'message': 'Login successful'}))
        response.set_cookie('access_token', token, httponly=True, secure=False, max_age=86400) #set secure=True for HTTPS
        return response
    else:
        return jsonify({'message': 'Enter valid credentials'}), 400
    
    
def protected(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch user details
        cursor.execute(f"SELECT image, username, name, email FROM users WHERE username = '{username}'")
        row = cursor.fetchone()

        conn.close()

        if row:
            return jsonify({
                'image': row[0],
                'username': row[1],
                'name': row[2],
                'email': row[3]
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': f'Error fetching user data: {str(e)}'}), 500
    
def logout():
    response = jsonify({'message': 'Logged out successfully'})
    response.set_cookie('access_token', '', expires=0, httponly=True, secure=False)  
    return response
