import uuid
from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory
get_worker_query = session.prepare("SELECT * FROM user_worker ;")


def get_workers():
    workers = session.execute(get_worker_query)
    return workers.all()


if __name__ == '__main__':
    print(get_workers())
