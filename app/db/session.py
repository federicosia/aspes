from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
DEFAULT_SESSION_FACTORY = sessionmaker(bind=engine)