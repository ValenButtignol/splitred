# Flask Entry Point

from flask import Flask
from flask_cors import CORS
from infrastructure.api.routes import register_routes
from infrastructure.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    # Enable CORS for all routes
    CORS(app)
    
    init_db()
    register_routes(app)
    return app

app = create_app()
