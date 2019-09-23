from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort, Blueprint)
import json
from app import dbi

# Initialise blueprints
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """
    Index page for database API.

    """
    return "API for database access."


@bp.route('/getuser', methods=['POST'])
def getuser():
    """
    Gets user from database and returns user data as JSON.

    """
    # Get data
    data = request.get_json()
    userid = data['userid']
    # Get user
    user = dbi.getuserbyid(userid)
    # If user is None, return false
    if user is None:
        return jsonify(success=False)
    # Convert user into dictionary
    data = {
        "userid": user.userid,
        "username": user.username
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
    username = data['username']
    password = data['password']
    # Create user
    success = dbi.createuser(username, password)
    # Return whether or not the user was created
    return jsonify(success=success)


@bp.route('/validateuser', methods=['POST'])
def validateuser():
    """
    Validates that the username and password matches.

    """
    # Get data
    data = request.get_json()
    username = data['username']
    password = data['password']
    # Validate user credentials
    success, userid = dbi.validateuser(username, password)
    # Return whether or not credentials are valid and the ID of the user
    return jsonify(success=success, userid=userid)