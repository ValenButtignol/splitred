# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///./splitred.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
