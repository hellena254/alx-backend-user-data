#!/usr/bin/env python3
""" Module for Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - List of all User objects in JSON format
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - user_id: ID of the User to retrieve
    Return:
      - JSON representation of the User object
      - 404 error if the User ID doesn't exist or is invalid
    """
    if user_id is None:
        abort(404)

    # Handle special case where user_id is "me"
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - user_id: ID of the User to delete
    Return:
      - Empty JSON if the User is successfully deleted
      - 404 error if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email: Email of the new User
      - password: Password for the new User
      - first_name: First name of the new User (optional)
      - last_name: Last name of the new User (optional)
    Return:
      - JSON representation of the newly created User
      - 400 error if the User can't be created due to invalid input
    """
    try:
        rj = request.get_json()
        if rj is None:
            return jsonify({'error': 'Invalid JSON format'}), 400

        # Validate required fields
        if not rj.get('email'):
            return jsonify({'error': 'Email is missing'}), 400
        if not rj.get('password'):
            return jsonify({'error': 'Password is missing'}), 400

        # Create and save the new User
        user = User(email=rj.get('email'), password=rj.get('password'),
                    first_name=rj.get('first_name'), last_name=rj.get('last_name'))
        user.save()
        return jsonify(user.to_json()), 201

    except Exception as e:
        return jsonify({'error': f'Could not create User: {str(e)}'}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - user_id: ID of the User to update
    JSON body:
      - first_name: Updated first name (optional)
      - last_name: Updated last name (optional)
    Return:
      - JSON representation of the updated User
      - 404 error if the User ID doesn't exist
      - 400 error if the update operation fails
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
        if rj is None:
            return jsonify({'error': 'Invalid JSON format'}), 400

        # Update fields if provided
        user.first_name = rj.get('first_name', user.first_name)
        user.last_name = rj.get('last_name', user.last_name)
        user.save()
        return jsonify(user.to_json()), 200

    except Exception as e:
        return jsonify({'error': f'Could not update User: {str(e)}'}), 400
