from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort)
from flask_login import LoginManager, current_user, login_user, logout_user
from app import dbi, login_manager
from app.main import bp


@login_manager.user_loader
def load_user(userid):
    # Query database for user
    user = dbi.getuserbyid(userid)
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
