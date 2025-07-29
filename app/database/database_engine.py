from flask_sqlalchemy import SQLAlchemy
from elasticsearch_dsl import connections
db = SQLAlchemy()

def init_elasticsearch():
    return connections.create_connection(
        hosts=[Config.ELASTIC_HOST],
        basic_auth=(Config.ELASTIC_USER, Config.ELASTIC_PASS),
        verify_certs=False,
        timeout=90
)
