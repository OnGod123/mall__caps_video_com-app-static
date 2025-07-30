from flask_sqlalchemy import SQLAlchemy
from elasticsearch_dsl import connections
from app.config.config import Config
db = SQLAlchemy()

def db_init_app(app):
    db.init_app(app)

def init_elasticsearch():
    return connections.create_connection(
        hosts=[Config.ELASTIC_HOST],
        basic_auth=(Config.ELASTIC_USER, Config.ELASTIC_PASS),
        verify_certs=False,
        timeout=90
)
