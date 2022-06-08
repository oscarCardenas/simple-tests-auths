from flask import Flask
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, HTTPDigestAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth(scheme='Bearer')

app.config['SECRET_KEY'] = 'secret'
authDigest = HTTPDigestAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@authBasic.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/auth_basic')
@authBasic.login_required
def index():
    return "Hello, {}!".format(authBasic.current_user())


tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@authToken.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/api_token')
@authToken.login_required
def index():
    return "Hello, {}!".format(authToken.current_user())



users = {
    "john": "hello",
    "susan": "bye"
}

@authDigest.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/auth_digest')
@authDigest.login_required
def index():
    return "Hello, {}!".format(authDigest.username())