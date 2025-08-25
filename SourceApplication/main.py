from flask import Flask, jsonify, render_template, request
import api.auth as auth
from config.jwt_config import SECRET_KEY, token_required
from config.logger_config import setup_logger

app = Flask(__name__) 
app.config['SECRET_KEY'] = SECRET_KEY

# Disable Flask default logs
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

logger = setup_logger()

# Log after every request with custom format
@app.after_request
def log_request_response(response):
    log_data = {
        "api_title": request.endpoint,
        "response_status": response.status_code,
    }
    logger.info("", extra=log_data)
    return response

@app.route('/auth/signup', methods=['POST'])
def add_user():
    return auth.signup()

@app.route('/auth/login', methods=['POST'])
def login():
    return auth.login()

@app.route('/auth/protected', methods=['GET'])
@token_required 
def protected(username):
    # return jsonify({'message': f'This is a protected route! {username}'})   
    return auth.protected(username)

@app.route('/auth/logout', methods=['POST'])
def logout():
    return auth.logout()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def signin():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/<path:anything>")
def not_found(anything):
    print(anything)
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
