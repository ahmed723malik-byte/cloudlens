"""
CloudLens - Multi-Cloud Infrastructure Visualiser & Cost Optimiser
A portfolio project demonstrating cloud architecture patterns and cost analysis.
"""

from flask import Flask
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .routes import main, api
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")

    return app
