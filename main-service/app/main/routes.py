from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort)
from flask_login import LoginManager, current_user, login_user, logout_user
from forms import UserLoginForm, UserRegistrationForm
from app import dbi, login_manager
from app.main import bp


@login_manager.user_loader
def load_user(userid):
    # Query database for user
    user = dbi.getuser(userid=userid)
    # Return user
    return user


@bp.route('/')
@bp.route('/index')
def index():
    """
    Landing page for users.

    """
    # Render index template
    return render_template('index.html')


@bp.route('/login')
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
        valid, userid = dbi.validateuser(username, password)
        # If valid, log user in and redirect to user index
        if valid:
            login_user(userid)
        else:
            flash("Invalid credentials.", category="error")
    # Render login template
    return render_template('login.html', form=form)


@bp.route('/registration')
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
        result = dbi.createuser(username, password)
        # If valid, log user in and redirect to user index
        if result:
            flash("Registration successful!", category="success")
            return redirect(url_for('login'))
        else:
            flash("Registration unsuccessful!", category="error")
    # Render registration page
    return render_template('registration.html', form=form)
