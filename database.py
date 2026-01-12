# src/database.py

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import orm

# ---------- Load environment ----------
load_dotenv()

db_user = os.getenv("DB_USER_NAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# ---------- Check for missing environment variables ----------
missing = [
    key
    for key, value in {
        "DB_USER_NAME": db_user,
        "DB_PASSWORD": db_password,
        "DB_HOST": db_host,
        "DB_PORT": db_port,
        "DB_NAME": db_name,
    }.items()
    if not value
]

if missing:
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

# ---------- Engine ----------
""" 
database connection string and quote_plus is used to escape special characters in the password.
"""
db_password_escaped = quote_plus(db_password)
DATABASE_URL = (
    f"postgresql+psycopg2://{db_user}:{db_password_escaped}"
    f"@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(DATABASE_URL, echo=True)

# ---------- Session factory ----------
"""
Create a session factory that will be used to create sessions.
"""
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# ---------- Helpers ----------
def create_tables() -> None:
    """
    Create all tables in the based on the ORM models.
    """
    try:
        orm.Base.metadata.create_all(engine)
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
        raise


def get_session():
    """
    Get a database session. Returns a session object that can be used to interact with the database.
    """
    try:
        return SessionLocal()
    except SQLAlchemyError as e:
        print(f"Error creating session: {e}")
        raise
