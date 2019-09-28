from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort)
from flask_login import LoginManager, current_user, login_user, logout_user
from app import usi, esi, login_manager
from app.main import bp
from app.main.forms import UserLoginForm, UserRegistrationForm


@login_manager.user_loader
def load_user(userid):
    # Query database for user
    user = usi.getuser(userid=userid)
    # Return user
    return user


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


@bp.routes('/events', methods=['GET', 'POST'])
def eventlist():
    """
    Page for events.

    """
    # Get events for current user
    events = esi.getuserevents(current_user.get_id())
    # Render template with events
    return render_template('eventlist.html', events=events)
