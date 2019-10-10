from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort, Blueprint)
import json
import requests
from datetime import timedelta, datetime
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
    # Query all events for the user sorted by start time
    query = db.collection('events')
    query = query.where('user_id', '==', data.get('user_id'))
    query = query.order_by('start_time', direction=firestore.Query.ASCENDING)
    events = query.stream()
    # Query all event warning for the user
    query = db.collection('event_warnings')
    query = query.where('user_id', '==', data.get('user_id'))
    warnings = query.stream()
    # Add events and warnings to dictionary
    data = dict()
    data['events'] = list()
    data['warnings'] = list()
    for event in events:
        event_dict = event.to_dict()
        event_dict.update({"id": event.id})
        data['events'].append(event_dict)
    for warning in warnings:
        warning_dict = warning.to_dict()
        warning_dict.update({"id": warning.id})
        data['warnings'].append(warning_dict)
    # Return event data
    return jsonify(data)


@bp.route('/addevent', methods=['POST'])
def addevent():
    """
    Adds event to database. Also generates warnings if events
    have time conflicts

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
    timestmp, added_event = db.collection('events').add({
        'address': str(data.get('address')),
        'description': str(data.get('description')),
        'start_time': parser.parse(data.get('start_time')),
        'end_time': parser.parse(data.get('end_time')),
        'title': str(data.get('title')),
        'travel_method': str(data.get('travel_method')),
        'user_id': str(data.get('user_id')),
    })
    # Generate any warnings the added event
    generatewarnings(added_event.get())
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
    # Get any warnings for the event and delete them
    warnings = db.collection('event_warnings').where(
        'from_event_id', '==', data.get('id')).stream()
    for warning in warnings:
        db.collection('event_warnings').document(warning.id).delete()
    warnings = db.collection('event_warnings').where(
        'to_event_id', '==', data.get('id')).stream()
    for warning in warnings:
        db.collection('event_warnings').document(warning.id).delete()
    # Return success
    return jsonify(success=True)


def generatewarnings(event_now):
    """
    Generates warnings if given event produces any time conflicts.

    """
    # Get user id of given event
    event_user_id = event_now.to_dict()['user_id']
    # Query all events for the user in order of start time
    query = db.collection('events')
    query = query.where('user_id', '==', event_user_id)
    query = query.order_by('start_time', direction=firestore.Query.ASCENDING)
    events = query.stream()
    # Iterate over each event and find any events before or after this one
    event_before = None
    event_after = None
    prev_event = None
    for event in events:
        if event.id == event_now.id:
            event_before = prev_event
        elif event_before is not None:
            event_after = event
            break
        prev_event = event
    # Call Google maps directions API to get the times between the events
    travel_time_to = timedelta(0)
    travel_time_from = timedelta(0)
    if event_before is not None:
        travel_time_to = timebetweenevents(event_before, event_now)
    if event_after is not None:
        travel_time_from = timebetweenevents(event_now, event_after)
    # If time between events is less than travel time between them with
    # a tolerance of one minute, create a suitable warning.
    # Check for time conflicts and generate warning for before and new events
    if event_before is not None:
        time_between_events = (event_now.to_dict()['start_time'] -
                               event_before.to_dict()['end_time'])
        if time_between_events < (travel_time_to - timedelta(minutes=1)):
            diff_min = (
                travel_time_to - time_between_events).total_seconds() // 60
            warning_message = (
                f"Time to get from event \"{event_before.to_dict()['title']}\""
                f" to \"{event_now.to_dict()['title']}\" by "
                f"{event_before.to_dict()['travel_method']} is {diff_min} "
                f"minutes more than between the end of first event and start "
                f"of the second event. Consider rescheduling events or "
                f"changing mode of transport.")
            db.collection('event_warnings').add({
                'from_event_id': event_before.id,
                'to_event_id': event_now.id,
                'user_id': event_user_id,
                'message': warning_message
            })
    # Check for time conflicts and generate warning for new and after events
    if event_after is not None:
        time_between_events = (event_after.to_dict()['start_time'] -
                               event_now.to_dict()['end_time'])
        if time_between_events < (travel_time_from - timedelta(minutes=1)):
            diff_min = int(
                travel_time_to - time_between_events).total_seconds() // 60
            warning_message = (
                f"Time to get from event \"{event_now.to_dict()['title']}\" "
                f"to \"{event_after.to_dict()['title']}\" by "
                f"{event_now.to_dict()['travel_method']} is {diff_min} "
                f"minutes more than between the end of first event and start "
                f"of the second event. Consider rescheduling events or "
                f"changing mode of transport.")
            db.collection('event_warnings').add({
                'from_event_id': event_now.id,
                'to_event_id': event_after.id,
                'user_id': event_user_id,
                'message': warning_message
            })


def timebetweenevents(fromevent, toevent):
    """
    Helper method for getting the estimated time between two events.
    Uses the fromevent's end_time and toevent's start_time for calculation.

    """
    # Get data for each event
    fromevent = fromevent.to_dict()
    toevent = toevent.to_dict()
    # Construct request address
    address = (f"https://maps.googleapis.com/maps/api/directions/json?"
               f"origin={fromevent['address']}"
               f"&destination={toevent['address']}"
               f"&mode={toevent['travel_method']}"
               f"&departure_time={int(fromevent['end_time'].timestamp())}"
               f"&key=AIzaSyCd4mRC2IuplYvR6O4U8XRr2VHsnk8LGNI")
    # Send request and get response
    response = requests.get(address)
    data = response.json()
    # Get total time of the first route if one exists
    travel_time = timedelta(0)
    if len(data['routes']) > 0:
        seconds = data['routes'][0]['legs'][0]['duration']['value']
        travel_time = timedelta(seconds=seconds)
    # Return travel time
    return travel_time
