from flask import Blueprint, request, jsonify, abort

from app import app
from app.auth.models import User


auth = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/auth/register/', methods=['POST'])
def register():
    """Registers users in the system"""
    username = request.json.get('username')
    password = request.json.get('password')
    # Prevent registeration without password
    if not username:
        return jsonify({
            "error": "Please supply a username in your request"
        }), 400
    # Prevent registeration without password
    if not password:
        return jsonify({
            "error": "Please supply a password in your request"
        }), 400

    # Fetch user records and verify the username is available
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            "error": "username already registered, choosse another"
        }), 400

    new_user = User(username, password)
    new_user.save()
    new_user.refresh_from_db()
    return jsonify({"success": "New user added successfully",
                    "username": new_user.username
                    }), 201


@app.route('/auth/login/', methods=['POST'])
def login():
    """"Logs in registered users"""
    username = request.json.get('username')
    password = request.json.get('password')
    # Prevent login without username
    if not username:
        return jsonify({
            "error": "Please supply a username in your request"
        }), 400
    # Prevent login without password
    if not password:
        return jsonify({
            "error": "Please supply a password in your request"
        }), 400

    # Fetch user records and verify credentials

    user = User.query.filter_by(username=username).first()

    if user and user.verify_password_hash(password):
        return jsonify({
            'message': 'Logged in successfully',
            'username': user.username,
            'token': user.generate_auth_token()
        })

    abort(401, {
        'error': {
            'message': 'Invalid credentials'
        }
    })
