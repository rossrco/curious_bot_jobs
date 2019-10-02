import os


def import_queries(query_dir):
    query_dir_path = os.path.join(os.path.dirname(__file__), query_dir)
    queries = {}
    for _file in (os.listdir(query_dir_path)):
        f_name, f_ext = os.path.splitext(_file)
        if f_ext == '.sql':
            with open(os.path.join(query_dir_path, _file), 'r') as query:
                queries[f_name] = query.read()
    return queries
