#!/usr/bin/env python3
"""
App module
"""

from flask import Flask, request, jsonify, abort
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user."""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        abort(400, description="Missing required fields")
    
    auth.register_user(email, password)
    
    return jsonify({
        "email": email,
        "message": "user created"
    }), 201

@app.route('/sessions', methods=['POST'])
def create_session():
    """Create a new session."""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        abort(400, description="Missing required fields")

    if not auth.valid_login(email, password):
        abort(401, description="Invalid credentials")
    
    session_id = auth.create_session(email)
    response = jsonify({
        "email": email,
        "message": "logged in"
    })
    response.set_cookie('session_id', session_id)
    
    return response

@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logout the current user."""
    session_id = request.cookies.get('session_id')
    
    if not session_id:
        abort(403, description="No session found")
    
    user = auth.get_user_from_session_id(session_id)
    
    if user is None:
        abort(403, description="Invalid session")
    
    auth.destroy_session(user.id)
    
    return jsonify({"message": "logged out"}), 200

@app.route('/profile', methods=['GET'])
def profile():
    """Retrieve the profile of the current user."""
    session_id = request.cookies.get('session_id')
    
    if not session_id:
        abort(403, description="No session found")
    
    user = auth.get_user_from_session_id(session_id)
    
    if user is None:
        abort(403, description="Invalid session")
    
    return jsonify({"email": user.email}), 200

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Generate a reset token for password reset."""
    email = request.form.get('email')
    
    if not email:
        abort(400, description="Missing required field")
    
    try:
        reset_token = auth.get_reset_password_token(email)
    except ValueError:
        abort(403, description="Email not registered")
    
    return jsonify({
        "email": email,
        "reset_token": reset_token
    }), 200

@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update the user's password using a reset token."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    
    if not email or not reset_token or not new_password:
        abort(400, description="Missing required fields")

    try:
        auth.update_password(reset_token, new_password)
    except ValueError:
        abort(403, description="Invalid reset token")
    
    return jsonify({
        "email": email,
        "message": "Password updated"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
