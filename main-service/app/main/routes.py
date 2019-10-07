from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort)
from flask_login import LoginManager, current_user, login_user, logout_user
from functools import wraps
from config import Config
from app import usi, esi, login_manager
from app.main import bp
from app.main.forms import (UserLoginForm, UserRegistrationForm, EventForm,
                            ProfileImageForm)
from datetime import time, date, datetime


@login_manager.user_loader
def load_user(userid):
    # Query database for user
    user = usi.getuser(userid=userid)
    # Return user
    return user


def user_login_required(f):
    """
    Decorator for routes that require a user to be logged in.

    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            # Flash warning that user login is required
            flash("User login required.", category="error")
            # Return redirect to login
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@bp.route('/index')
def index():
    """
    Landing page for users.

    """
    # Check if user is currently logged in
    if current_user.is_authenticated:
        # Render index page
        return render_template('index.html', user=current_user)
    else:
        # Render landing page
        return render_template('landing.html')


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Page for registration as a user.

    """
    # Initialise registration form
    form = UserRegistrationForm()
    # Process login form if submitted
    if form.validate_on_submit():
        # Get field values
        username = form.username.data
        password = form.password.data
        # Create user
        result = usi.createuser(username, password)
        # If valid, log user in and redirect to user index
        if result:
            flash("Registration successful!", category="success")
            return redirect(url_for('main.login'))
        else:
            flash("Registration unsuccessful!", category="error")
    # Render registration page
    return render_template('registration.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Page for login as user.

    """
    # Initialise login form
    form = UserLoginForm()
    # Process login form if submitted
    if form.validate_on_submit():
        # Get field values
        username = form.username.data
        password = form.password.data
        # Validate credentials
        valid = usi.validateuser(username, password)
        # If valid, log user in and redirect to user index
        if valid:
            user = usi.getuser(username=username)
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash("Invalid credentials.", category="error")
    # Render login template
    return render_template('login.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Handles user logouts.

    """
    # Log user out
    logout_user()
    # Redirect to landing page
    return redirect(url_for('main.index'))


@bp.route('/profile')
@user_login_required
def userprofile():
    """
    Page for user to modify their details.

    """
    # Get profile image link for user
    profile_image_link = usi.getuserimagelink(current_user.get_id())
    # Create and define image upload form
    imageform = ProfileImageForm()
    # Render user page
    return render_template('userprofile.html', user=current_user,
                           imageform=imageform,
                           profile_image_link=profile_image_link)


@bp.route('/profile/upload-profile-image', methods=['POST'])
@user_login_required
def uploaduserprofileimage():
    """
    Page for receiving a user's profile image.

    """
    # Define form
    form = ProfileImageForm()
    # Check that file is contained in post
    if form.validate_on_submit:
        # Get file
        file = form.image.data
        # Upload file to storage
        success = usi.adduserimage(current_user.get_id(), file)
        # Check that image upload was successful
        if success:
            # Flash success
            flash("Profile image successfully changed", category="success")
    # Redirect to user page
    return redirect(url_for('main.userprofile'))


@bp.route('/events')
@user_login_required
def eventlist():
    """
    Page for events.

    """
    # Get events for current user
    events, warnings = esi.getuserevents(current_user.get_id())
    # Get options
    options = request.args
    # Cull event list depending on options
    if options.get('list') == "all":
        # Remove nothing from list
        pass
    else:
        # Remove all events that have already happened (Default)
        now = datetime.now()
        events = [event for event in events if event['start_time'] > now]
    # Render template with events
    return render_template('eventlist.html', events=events, warnings=warnings)


@bp.route('/event/<id>/delete')
@user_login_required
def deleteevent(id):
    """
    Deletes specified event.

    """
    # Delete given event
    deleted = esi.deleteevent(id)
    # If successful or error occured, flash message or warning
    if deleted:
        flash("Event deleted successfully", category="success")
    else:
        flash("Event could not be deleted", category="error")
    # Redirect to event list
    return redirect(url_for('main.eventlist'))


@bp.route('/events/create')
@user_login_required
def addevent():
    # Define form
    form = EventForm()
    # Render template with form
    return render_template('eventform.html', form=form)


@bp.route('/events/create/submit', methods=['POST'])
@user_login_required
def addeventsubmit():
    # Define form
    form = EventForm()
    # Process form
    if form.validate_on_submit():
        # Get data
        title = form.title.data
        description = form.description.data
        address = form.address.data
        user_id = current_user.get_id()
        start_time = datetime.combine(
            form.start_date.data, form.start_time.data)
        end_time = datetime.combine(
            form.end_date.data, form.end_time.data)
        travel_method = form.travel_method.data
        # Create event
        esi.addevent(title=title, description=description, user_id=user_id,
                     address=address, start_time=start_time, end_time=end_time,
                     travel_method=travel_method)
        # Redirect to event list
        return redirect(url_for('main.eventlist'))
    else:
        # Flash all form errors
        for field, errormessages in form.errors.items():
            for errormessage in errormessages:
                flash(errormessage, category="error")
        # Redirect to event list
        return redirect(url_for('main.addevent'))
