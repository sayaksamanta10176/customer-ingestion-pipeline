import os
from dotenv import load_dotenv

# loading all .env values
load_dotenv()

from cryptography.fernet import Fernet

SECRET_KEY = os.getenv("SECRET_KEY")
cipher_suite = Fernet(SECRET_KEY.encode())

# Function to decrypt the values
def decrypt_value(encrypted_value):
    if encrypted_value is None:
        return None
    return cipher_suite.decrypt(encrypted_value.encode()).decode()

# Loading the db credentials
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Decrypting credentials
db_user = decrypt_value(DB_USER)
db_pass = decrypt_value(DB_PASS)
db_host = decrypt_value(DB_HOST)
db_name = decrypt_value(DB_NAME)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Sqlalchemy database url
DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

# Starting the engine
engine = create_engine(DATABASE_URL)

# This will create a db session on function call
SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()