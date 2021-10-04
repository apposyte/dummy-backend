import json
import traceback
from configparser import ConfigParser

from elasticsearch import Elasticsearch

try:
    # Configuration
    config = ConfigParser()
    config.read('configuration.ini')

    data = json.load(open('./data/sample-data.json', 'r'))

    es_client = Elasticsearch([{'host': config.get('DEFAULT', 'host'), 'port': config.get('DEFAULT', 'port')}])

    for id, record in enumerate(data):
        es_client.index(index='%s' % config.get('DEFAULT', 'index'), doc_type='_doc', id=id, body=record)

except Exception as exception:
    print(exception)
    traceback.print_exc()