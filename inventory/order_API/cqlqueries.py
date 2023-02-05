from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory

get_orders_query = session.prepare("SELECT pid,numbers,timestamp FROM orders ;")


def get_orders():
    orders = session.execute(get_orders_query).all()
    return orders


if __name__ == '__main__':
    a = get_orders()
    print(a)
