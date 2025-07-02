from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from infrastructure.db.models import Base

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
