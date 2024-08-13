#!/usr/bin/env python3
""" Module for user authentication and session management
"""

import os
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """
    Handles user login by creating a session for valid credentials.

    Returns:
        Response: JSON response indicating the result of the login attempt.
            - 400 if email or password is missing.
            - 404 if no user is found with the provided email.
            - 401 if the password is incorrect.
            - 200 with user data and session cookie if login is successful.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response
    
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out the user by destroying the current session.

    Returns:
        Response: JSON response indicating the result of the logout attempt.
            - 200 if the session was successfully destroyed.
            - 404 if the session could not be destroyed.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    
    abort(404)
