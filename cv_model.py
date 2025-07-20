from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Use SQLite (local file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "cv_database.db")
engine = create_engine(f'sqlite:///{db_path}', echo=False)

Base = declarative_base()

class CVUpload(Base):
    __tablename__ = 'cv_uploads'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filepath = Column(String)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
