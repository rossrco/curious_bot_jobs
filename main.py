import logging

from flask import Flask
import feedparser
import yaml

import pandas as pd

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
    rss_url = config['stack_overflow_rss']
    feed = feedparser.parse(rss_url)

    data = utils.convert_feed_to_frame(feed)

    try:
        latest_ad_date = bq_client.query(latest_ad_date_query).result()
    except google_exceptions.NotFound:
        latest_ad_date = None

    if latest_ad_date and latest_ad_date < data.published.max():
        new_data = data[data.published > latest_ad_date].copy()
        return f'Saving {len(new_data)} new records.'
    else:
        return f'Saving {len(data)} new records.'


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.INFO)

    app.run(host='127.0.0.1', port=8080, debug=True)
