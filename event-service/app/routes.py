from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort, Blueprint)
import json
from dateutil import parser
from app import db

# Initialise blueprints
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """
    Index page for database API.

    """
    return "API for events."


@bp.route('/getuserevents', methods=['POST'])
def getuserevents():
    """
    Gets all events for a given user.

    """
    # Get data from JSON
    data = request.get_json()
    # If nethier field is specified, return failure
    if not data.get('user_id'):
        return jsonify(success=False,
                       messages=["User id must be specified."])
    # Query all events
    events = db.collection('events').where(
        'user_id', '==', data.get('user_id')).stream()
    # Add events to dictionary
    data = dict()
    data['events'] = dict()
    for event in events:
        data['events'][event.id] = event.to_dict()
    # Return event data
    return data


@bp.route('/addevent', methods=['POST'])
def addevent():
    """
    Adds event to database.

    """
    # Get data from JSON
    data = request.get_json()
    # Ensure all required fields are provided
    valid = True
    messages = list()
    if not data.get('user_id'):
        valid = False
        messages.append("User id required.")
    if not data.get('title'):
        valid = False
        messages.append("Event title required.")
    if not data.get('time'):
        valid = False
        messages.append("Event datetime required.")
    # If given data is invalid, return failure with errors
    if not valid:
        return jsonify(success=False, messages=messages)
    # Add event
    db.collection('events').add({
        'address': str(data.get('address')),
        'description': str(data.get('description')),
        'time': parser.parse(data.get('time')),
        'title': str(data.get('title')),
        'travel_method': str(data.get('travel_method')),
        'user_id': str(data.get('user_id')),
    })
    # Return success
    return jsonify(success=True)
