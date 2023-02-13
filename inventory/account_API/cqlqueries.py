import uuid
from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory
get_worker_query = session.prepare("SELECT * FROM user_worker ;")
create_worker_query = session.prepare(
    "INSERT INTO user_worker (pid , fname , lname , password  ) VALUES ( ?, ?,?, ?) ;")


def get_workers():
    workers = session.execute(get_worker_query)
    return workers.all()


def create_worker(f_name, l_name, password, pid=None):
    if pid is None:
        pid = uuid.uuid4()
    session.execute(create_worker_query, (pid, f_name, l_name, password))


if __name__ == '__main__':
    print(get_workers())
