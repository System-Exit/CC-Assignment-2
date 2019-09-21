from flask import Blueprint

# Initialise blueprints
bp = Blueprint('main', __name__)

# Import routes
from app.main import routes  # nopep8
