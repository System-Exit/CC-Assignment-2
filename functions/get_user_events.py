"""
Requirements:
flask>=1.1.1
requests>=2.22.0

"""
import requests


def get_user_events(request):
    """
    Takes a HTTP JSON request and returns a JSON array
    of all events for a given user. This is simply a proxy,
    to another microservice, due to issues faced initialising
    firestore in google cloud functions.
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
    # Call event service to get events
    url = "https://event-dot-lustrous-oasis-253108.appspot.com/getuserevents"
    response = requests.post(url, json={"user_id": request.get('id')})
    data = response.json()
    # Return JSON of events
    return jsonify(data['events'])
