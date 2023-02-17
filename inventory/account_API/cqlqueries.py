from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory
get_workers_query = session.prepare("SELECT username , fname , lname FROM user_worker ;")
get_admins_query = session.prepare("SELECT username , fname , lname FROM user_admin ;")
create_worker_query = session.prepare(
    "INSERT INTO user_worker (username , fname , lname , password  ) VALUES ( ?, ?,?, ?) IF NOT EXISTS;")
create_admin_query = session.prepare(
    "INSERT INTO user_admin (username , fname , lname , password  ) VALUES ( ?, ?,?, ?) IF NOT EXISTS;")
get_worker_query = session.prepare("SELECT username , fname , lname FROM user_worker WHERE username = ? LIMIT 1; ")
get_admin_query = session.prepare("SELECT username , fname , lname FROM user_admin WHERE username = ? LIMIT 1; ")
update_worker_query = session.prepare("UPDATE user_worker SET fname = ? , lname = ? WHERE username = ? IF EXISTS ;")


class AlreadyExists(Exception):
    pass


def get_workers(username=None):
    if username is None:
        workers = session.execute(get_workers_query)
        return workers.all()
    else:
        worker = session.execute(get_worker_query, (username,)).one()
        return worker


def create_worker(f_name, l_name, password, username=None):
    if username is None:
        username = f_name + l_name
    a = session.execute(create_worker_query, (username, f_name, l_name, password)).one()
    return a['[applied]']


def update_worker(f_name, l_name, username):
    return session.execute(update_worker_query, (f_name, l_name, username)).one()['[applied]']


def get_admins(username=None):
    if username is None:
        admin = session.execute(get_admins_query)
        return admin.all()
    else:
        admin = session.execute(get_admin_query, (username,)).one()
        return admin


def create_admin(f_name, l_name, password, username=None):
    if username is None:
        username = f_name + l_name
    a = session.execute(create_admin_query, (username, f_name, l_name, password)).one()
    return a['[applied]']


if __name__ == '__main__':
    # print(get_workers())
    print(update_worker('a', 'a', 'a'))
