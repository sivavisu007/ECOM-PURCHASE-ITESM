from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os 
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)
sessionlocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)
Base = declarative_base()