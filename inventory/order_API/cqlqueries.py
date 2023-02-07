import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
from build_API import cqlqueries as build_cql

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory

get_orders_query = session.prepare("SELECT pid,numbers,timestamp FROM orders ;")
insert_into_orders_query = session.prepare(
    "INSERT INTO orders (date , pid , timestamp , numbers ) VALUES ( ? , ?,?, ? ) ;")
get_order_number_query = session.prepare("SELECT numbers FROM orders WHERE date= ? AND  pid = ? ")
get_order_query = session.prepare("SELECT pid , numbers, timestamp  FROM orders WHERE date = ? AND pid = ? ;")
edit_order_query = session.prepare("UPDATE orders SET numbers = ? WHERE date = ? AND pid = ? IF EXISTS;")


def get_orders():
    orders = session.execute(get_orders_query).all()
    return orders


def get_order(date, pid):
    date = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    order = session.execute(get_order_query, (date, pid)).one()
    if order is not None:
        return order
    else:
        return None


def get_order_number(date, pid):
    date = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    numbers = session.execute(get_order_number_query, (date, pid)).one()
    if numbers is not None:
        return numbers['numbers']
    else:
        return None


def add_order(pid, date, numbers):
    order_numbers = get_order_number(date=date, pid=pid)
    if order_numbers is not None:
        order_numbers = order_numbers + numbers
        build_cql.add_needed(pid, numbers)
        edit_orders(pid=pid, ts=date, numbers=order_numbers)


def remove_order(pid, date, numbers):
    order_numbers = get_order_number(date=date, pid=pid)
    if order_numbers is not None and order_numbers >= numbers:
        order_numbers = order_numbers - numbers
        edit_orders(pid=pid, ts=date, numbers=order_numbers)


def edit_orders(pid, ts, numbers=1):
    dt = datetime.fromtimestamp(ts)
    session.execute(edit_order_query, (numbers, dt, pid))


def complete_order(pid, date, numbers):
    order_numbers = get_order_number(date=date, pid=pid)
    if order_numbers is not None and order_numbers >= numbers:
        try:
            build_cql.discard_stock(pid, numbers)
            build_cql.remove_needed(pid, numbers)
            remove_order(pid=pid, date=date, numbers=numbers)
        except build_cql.InvalidNumber:
            return build_cql.get_stock(pid) - numbers

        # edit_orders(pid=pid, ts=date, numbers=order_numbers)


if __name__ == '__main__':
    # a = add_order(date=1675595420, pid=uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e'), numbers=1)
    # a = get_order_number(date=1675595420, pid=uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e'))
    # print(a)
    complete_order(pid=uuid.UUID('6a9dbb20-a4b5-11ed-97fb-f889d2e645af'), date=1675595420, numbers=12)
