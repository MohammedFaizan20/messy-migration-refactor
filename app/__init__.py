from flask import Flask
from .models import init_db
from .routes import bp
import os

def create_app():
    app = Flask(__name__)

    # Initialize the database only if it doesn't exist
    if not os.path.exists('users.db'):
        init_db()

    app.register_blueprint(bp)

    return app
