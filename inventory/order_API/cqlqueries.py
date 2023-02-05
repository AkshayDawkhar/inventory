import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory

get_orders_query = session.prepare("SELECT pid,numbers,timestamp FROM orders ;")
insert_into_orders_query = session.prepare(
    "INSERT INTO orders (date , pid , timestamp , numbers ) VALUES ( ? , ?,?, ? ) ;")


def get_orders():
    orders = session.execute(get_orders_query).all()
    return orders


def edit_orders(pid, ts, numbers=1):
    dt = datetime.fromtimestamp(ts)
    session.execute(insert_into_orders_query, (dt, pid, dt, numbers))


if __name__ == '__main__':
    a = edit_orders(uuid.UUID('db111c18-222b-4914-a108-b3e759239c5e'), 1675595420, 1)
