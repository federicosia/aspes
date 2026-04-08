from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

engine = create_engine(settings.database_url)
DEFAULT_SESSION_FACTORY = sessionmaker(bind=engine)