# Flask Entry Point

from flask import Flask
from flask_cors import CORS
from infrastructure.api.routes import register_routes
from infrastructure.db import init_db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import FRONTEND_URL

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    limiter = Limiter(get_remote_address, app=app, default_limits=["60 per minute"])
    
    # Enable CORS for all routes
    CORS(app, origins=FRONTEND_URL)
    
    init_db()
    register_routes(app, limiter)
    return app

app = create_app()