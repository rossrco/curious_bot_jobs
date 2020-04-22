import os
import pandas as pd


def import_queries(query_dir):
    query_dir_path = os.path.join(os.path.dirname(__file__), query_dir)
    queries = {}
    for _file in (os.listdir(query_dir_path)):
        f_name, f_ext = os.path.splitext(_file)
        if f_ext == '.sql':
            with open(os.path.join(query_dir_path, _file), 'r') as query:
                queries[f_name] = query.read()
    return queries


def convert_feed_to_frame(feed):
    feed_frame = pd.DataFrame(feed.entries)
    data = feed_frame[['id', 'author', 'location',
                       'published', 'tags', 'title',
                       'summary_detail']].copy()
    data['published'] = pd.to_datetime(data['published'])
    data['tags'] = [[tag['term'] for tag in tags]
                    if isinstance(tags, list)
                    else [] for tags in data.tags]
    data['description'] = [entry['value'] for entry in data['summary_detail']]
    data.drop('summary_detail', axis=1, inplace=True)
    return data
