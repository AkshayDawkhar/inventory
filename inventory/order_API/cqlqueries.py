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
get_order_number_query = session.prepare("SELECT numbers FROM orders WHERE date= ? AND  pid = ? ")


def get_orders():
    orders = session.execute(get_orders_query).all()
    return orders


def get_order_number(date, pid):
    date = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    numbers = session.execute(get_order_number_query, (date, pid)).one()
    if numbers is not None:
        return numbers['numbers']
    else:
        return None


def edit_orders(pid, ts, numbers=1):
    dt = datetime.fromtimestamp(ts)
    session.execute(insert_into_orders_query, (dt, pid, dt, numbers))


if __name__ == '__main__':
    # a = edit_orders(uuid.UUID('db111c18-222b-4914-a108-b3e759239c5e'), 1675595420, 1)
    a = get_order_number(date=1675595420, pid=uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e'))
    print(a)
