from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort, Blueprint)
import json
from app import db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialise blueprints
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """
    Index page for database API.

    """
    return "API for users."


@bp.route('/getuser', methods=['POST'])
def getuser():
    """
    Gets user from database and returns user data as JSON.
    Either 'id' or 'username' must be specified, with 'id'
    taking priority on what will be searched.

    """
    # Get data from JSON
    data = request.get_json()
    # If nethier field is specified, return failure
    if not data.get('id') and not data.get('username'):
        return jsonify(success=False,
                       messages=["Username or id must be specified."])
    # Get user by id if specified
    elif data.get('id'):
        id = str(data.get('id'))
        user = db.collection('users').document(id).get()
        # If user is not found, return failure
        if user.exists is False:
            return jsonify(success=False,
                           messages=["User with id not found."])
    # Get user by username if specified
    elif data.get('username'):
        username = str(data.get('username'))
        user = check_collection_contains(
            db.collection('users'), 'username', username)
        if not user:
            return jsonify(success=False,
                           messages=["User with id not found."])
    # Convert user into dictionary
    data = {
        "id": user.id,
        "username": user.to_dict()['username']
    }
    # Return user info in JSON
    return jsonify(data)


@bp.route('/createuser', methods=['POST'])
def createuser():
    """
    Adds new user to database based on JSON data.

    """
    # Get data
    data = request.get_json()
    # Check that all required fields are included
    if not data.get('username') or not data.get('password'):
        return jsonify(success=False,
                       messages=["Username and password required"])
    # Assign user variables
    username = str(data['username'])
    password = str(data['password'])
    # Check that username is unique
    user = check_collection_contains(
        db.collection('users'), 'username', username)
    if user is not None:
        return jsonify(success=False,
                       messages=["Username already taken"])
    # Hash password
    passhash = PasswordHasher().hash(password)
    # Create and add user to database
    db.collection('users').add({
        'username': username,
        'passhash': passhash
    })
    # Return success
    return jsonify(success=True)


@bp.route('/validateuser', methods=['POST'])
def validateuser():
    """
    Validates that the username and password matches.

    """
    # Get data
    data = request.get_json()
    # Check that all required fields are included
    if not data.get('username') or not data.get('password'):
        return jsonify(success=False,
                       messages=["Username and assword required"])
    # Assign user variables
    username = str(data['username'])
    password = str(data['password'])
    # Get user
    user = check_collection_contains(
        db.collection('users'), 'username', username)
    # Check that user exists
    if user is None:
        return jsonify(success=False,
                       messages=["User does not exist"])
    # Verify whether or not password is valid
    try:
        valid = PasswordHasher().verify(user.to_dict()['passhash'], password)
    except VerifyMismatchError:
        return jsonify(success=False,
                       messages=["Invalid password"])
    # Return success
    return jsonify(success=True)


def check_collection_contains(col_ref, field, value):
    """
    Checks if a collection contains any objects where the field has
    the passed value.

    Args:
        col_ref: Collection reference to query.
        field (str): Field to search for.
        value (str): Value of field to search for.
    Returns:
        Document snapshot of first item if one exists.
        None if collection has not documents that match query.

    """
    # Check if item that matches field and value exists in collection
    try:
        item = next(col_ref.where(field, '==', value).stream())
    # Since no item exists, return None
    except StopIteration:
        return None
    # Return item
    return item
