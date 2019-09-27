# get date last modified (if available)
# parse all rss entries after date last modified
# wrangle entries data
# save data to bigquery

import logging

from flask import Flask
import feedparser
import yaml


config = yaml.safe_load(open('config.yaml', 'r'))


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Nothing to see here, move along!'


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.INFO)

    app.run(host='127.0.0.1', port=8080, debug=True)
