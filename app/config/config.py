import os
from dotenv import load_dotenv

load_dotenv()  # Loads from .env by default

class Config:
    # Flask secret
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # Elasticsearch
    INDEX_NAME = os.getenv("INDEX_NAME")
    INDEX_NAME_2 = os.getenv("INDEX_NAME_2")
    ELASTIC_HOST = os.getenv("ELASTIC_HOST")
    ELASTIC_USER = os.getenv("ELASTIC_USER")
    ELASTIC_PASS = os.getenv("ELASTIC_PASS")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_DECODE_RESPONSES = os.getenv("REDIS_DECODE_RESPONSES", "True").lower() == "true"

    #Open_api
    Opem_api_key = os.getenv("Open_api_key")
