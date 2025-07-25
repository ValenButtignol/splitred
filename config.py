# Centralized Configuration
import os

#DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.sqlite3")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./splitred.db")
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@<host>:<port>/splitred")

FRONTEND_URL = "http://192.168.1.18:5173"

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB