import logging

from flask import Flask
import feedparser
import yaml

from google.cloud import bigquery
import google.api_core.exceptions as google_exceptions

import utils


config = yaml.safe_load(open('config.yaml', 'r'))


queries = utils.import_queries('queries')


bq_client = bigquery.Client()


app = Flask(__name__)


@app.route('/')
def hello():
    
    latest_ad_date_query = queries['get_latest_ad_date']
    try:
        latest_ad_date = bq_client.query(latest_ad_date_query).result()
        return latest_ad_date.strftime(format='%Y-%m-%d')
    except google_exceptions.NotFound:
        return 'The table does not exist'


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.INFO)

    app.run(host='127.0.0.1', port=8080, debug=True)
