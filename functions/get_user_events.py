from flask import jsonify
import firebase_admin
from firebase_admin import credentials, firestore


def get_user_events(request):
    """
    Takes a HTTP JSON request and returns a JSON array
    of all events for a given user.
    Args:
        request (flask.Request): HTTP request object.
        This request should be a JSON specifing the ID
        of the user that this function should return.
        Format: {'id': '<user ID>'}

    Returns:
        All of the data for each event associated with
        the given user ID in JSON format.
    """
    # Get request
    request = request.get_json()
    # If nethier field is specified, return failure
    if not request.get('id'):
        return jsonify(success=False,
                       messages=["User id must be specified."])
    # Load database interface
    creds = credentials.ApplicationDefault()
    firebase_admin.initialize_app(creds)
    db = firestore.client()
    # Query all events for the user sorted by start time
    query = db.collection('events')
    query = query.where('user_id', '==', request.get('id'))
    query = query.order_by('start_time', direction=firestore.Query.ASCENDING)
    events = query.stream()
    # Add events to dictionary
    events = list()
    for event in events:
        event_dict = event.to_dict()
        event_dict.update({"id": event.id})
        events.append(event_dict)
    # Return event data
    return jsonify(events)
