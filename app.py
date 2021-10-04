import traceback
from configparser import ConfigParser

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from flask import Flask, Response

# Configuration
config = ConfigParser()
config.read('configuration.ini')

app = Flask(__name__)

# @app.route("/")
# def index():
#     return "Hello world!"

@app.route("/")
def index():

    try:

        es_client =  Elasticsearch([{ 'host': config.get('DEFAULT', 'host'), 'port': config.get('DEFAULT', 'port') }])

        query_object = Search()\
            .using(es_client)\
            .index(config.get('DEFAULT', 'index'))\
            .query("match", gender="female")

        query_result = query_object.execute()

        response_object = query_result.to_dict()

        response_string = '<html><head>Sample Elastic query results</head><body><ul>'
        if 'hits' in response_object and 'hits' in response_object['hits'] and len(response_object['hits']['hits']) > 0:
            for hit in response_object['hits']['hits']:
                response_string += '<li>Name: ' + str(hit['_source']['name']) + ' (Age:' + str(hit['_source']['age']) + ')</li>'

        response_string += '</ul></body></html>'

        return response_string

    except Exception as exception:
        print(exception)
        traceback.print_exc()
        return Response("", status=503, mimetype='application/json')
    return json.dumps(response)
