from configparser import ConfigParser

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from flask import Flask

# Configuration
config = ConfigParser()
config.read('configuration.ini')

# Query
query_definition = {
    "bool": {
        "must": [{'gender': 'female'}]
}}

app = Flask(__name__)

@app.route("/")
def index():

    es_client =  Elasticsearch([{ 'host': config.get('DEFAULT', 'host'), 'port': config.get('DEFAULT', 'port') }])

    query_object = Search()
    query_object = query_object.query(query_definition)
    query_object = query_object.using(es_client)
    query_object = query_object.index(config.get('DEFAULT', 'index'))
    query_result = query_object.execute()

    return query_result.to_dict()
