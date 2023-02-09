import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
from build_API import cqlqueries as build_cql

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory

# create_order_query = session.prepare("INSERT INTO orders (date , pid , numbers ) VALUES ( ?, ?, ? ) ;")
get_orders_query = session.prepare("SELECT pid,numbers,timestamp FROM orders ;")
insert_into_orders_query = session.prepare(
    "INSERT INTO orders (date , pid , timestamp , numbers ) VALUES ( ? , ?,?, ? ) ;")
get_order_number_query = session.prepare("SELECT numbers FROM orders WHERE date= ? AND  pid = ? ")
get_order_query = session.prepare("SELECT pid , numbers, timestamp  FROM orders WHERE date = ? AND pid = ? LIMIT 1 ;")
edit_order_query = session.prepare("UPDATE orders SET numbers = ? WHERE date = ? AND pid = ? IF EXISTS;")
get_orders_by_pid_query = session.prepare("SELECT pid , numbers, timestamp FROM orders_by_pid WHERE pid = ? ;")
get_orders_by_date_query = session.prepare("SELECT pid , numbers, timestamp FROM orders WHERE date = ? ;")
get_order_number_by_pid_query = session.prepare("SELECT numbers FROM orders_by_pid WHERE pid = ? ;")


def create_order(pid, date, numbers=1):
    date_no = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    date = datetime.fromtimestamp(date)
    session.execute(insert_into_orders_query, (date_no, pid, date, numbers))


def get_orders():
    orders = session.execute(get_orders_query).all()
    return orders


def get_order(date=None, pid=None):
    if date is not None and pid is not None:
        date = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        order = session.execute(get_order_query, (date, pid)).one()
        if order is not None:
            return order
        else:
            return None
    elif date is not None and pid is None:
        date = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        orders = session.execute(get_orders_by_date_query, (date,)).all()
        return orders
    elif pid is not None and date is None:
        orders = session.execute(get_orders_by_pid_query, (pid,)).all()
        return orders
    else:
        orders = session.execute(get_orders_query).all()
        return orders


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
    else:
        build = build_cql.get_build(pid)
        create_order(pid=pid, date=date, numbers=numbers)


def remove_order(pid, date, numbers):
    order_numbers = get_order_number(date=date, pid=pid)
    if order_numbers is not None and order_numbers >= numbers:
        order_numbers = order_numbers - numbers
        edit_orders(pid=pid, ts=date, numbers=order_numbers)
        # add_need(pid)


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


def get_orders_by_pid(pid):
    orders = session.execute(get_orders_by_pid_query, (pid,)).all()
    return orders


def add_need(pid):
    numbers = session.execute(get_order_number_by_pid_query, (pid,)).all()
    number = sum([n['numbers'] for n in numbers])
    build_cql.update_needed(rid=pid, needed=number)


if __name__ == '__main__':
    # a = add_order(date=1675595420, pid=uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e'), numbers=1)
    # a = get_order_number(date=1675595420, pid=uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e'))
    # print(a)
    # complete_order(pid=uuid.UUID('6a9dbb20-a4b5-11ed-97fb-f889d2e645af'), date=1675595420, numbers=12)
    # print(get_orders_by_pid(pid=uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e')))
    # print(get_order(pid=uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e')))
    # print(get_order(date=1675569998))
    print(add_need(uuid.UUID('db656c18-222b-4914-a108-b3e759239c5e')))
