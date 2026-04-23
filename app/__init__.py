from flask import Flask
from app.extensions import db
from app.routes import main

def create_app(config=None):
    app = Flask(__name__)

    # Default config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override with test config
    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(main)

    # Create tables for testing
    with app.app_context():
        db.create_all()

    return app