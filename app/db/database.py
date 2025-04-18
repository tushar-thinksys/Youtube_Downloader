# Placeholder for future database setup
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = "postgresql://postgres:tushar@localhost:5432/yt_downloader"

engine = create_engine(DATABASE_URL, echo=True)

#def init_db():
 #   SQLModel.metadata.create_all(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
