# Centralized Configuration
import os

#DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.sqlite3")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./splitred.db")
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@<host>:<port>/splitred")



class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
