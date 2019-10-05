from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort, Blueprint)
import json
from dateutil import parser
from app import db
from firebase_admin import firestore

# Initialise blueprints
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """
    Index page for database API.

    """
    return "API for events."


@bp.route('/getevent', methods=['POST'])
def getevent():
    """
    Gets event with given ID.

    """
    # Get data from JSON
    data = request.get_json()
    # Ensure all required fields are provided
    if not data.get('id'):
        return jsonify(success=False, messages=['Event ID required'])
    # Get event
    event = db.collection('events').document(data.get('id')).get()
    # Ensure that event exists
    if not event.exists:
        return jsonify(success=False, messages=['Event does not exist'])
    # Get event data
    data = {"id": event.id}
    data.update(event.to_dict())
    # Return event
    return jsonify(data)


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
    # Query all events for the user
    query = db.collection('events')
    query = query.where('user_id', '==', data.get('user_id'))
    # Sort query by time of event
    query = query.order_by('start_time', direction=firestore.Query.ASCENDING)
    # Get stream of events
    events = query.stream()
    # Add events to dictionary
    data = list()
    for event in events:
        event_dict = event.to_dict()
        event_dict.update({"id": event.id})
        data.append(event_dict)
    # Return event data
    return jsonify(data)


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
    if not data.get('start_time'):
        valid = False
        messages.append("Event start datetime required.")
    if not data.get('end_time'):
        valid = False
        messages.append("Event end datetime required.")
    # If given data is invalid, return failure with errors
    if not valid:
        return jsonify(success=False, messages=messages)
    # Add event
    db.collection('events').add({
        'address': str(data.get('address')),
        'description': str(data.get('description')),
        'start_time': parser.parse(data.get('start_time')),
        'end_time': parser.parse(data.get('end_time')),
        'title': str(data.get('title')),
        'travel_method': str(data.get('travel_method')),
        'user_id': str(data.get('user_id')),
    })
    # Return success
    return jsonify(success=True)


@bp.route('/deleteevent', methods=['POST'])
def deleteevent():
    """
    Remove event from database.

    """
    # Get data from JSON
    data = request.get_json()
    # Ensure all required fields are provided
    if not data.get('id'):
        return jsonify(success=False, messages=['Event ID required'])
    # Get event
    event = db.collection('events').document(data.get('id')).get()
    # Ensure that event exists
    if not event.exists:
        return jsonify(success=False, messages=['Event does not exist'])
    # Delete event from events
    db.collection('events').document(data.get('id')).delete()
    # Return success
    return jsonify(success=True)
