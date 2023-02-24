from datetime import date as dates
from datetime import datetime
import uuid

from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory


class DatabaseError(Exception):
    """
    The base error that functions in this module will raise when things go
    wrong.
    """
    pass


class NotFound(DatabaseError):
    pass


class Conflict(Exception):
    pass


class InvalidDictionary(DatabaseError):
    pass


class InvalidNumber(Exception):
    pass


cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory
create_build_query = session.prepare(
    "INSERT INTO product_builds (pid , building , instock , needed , recommended ) VALUES ( ?,?,?,?,?) ;")
get_builds_query = session.prepare("SELECT * FROM product_builds ;")
get_build_query = session.prepare("SELECT * FROM product_builds WHERE pid = ? LIMIT 1;")
get_req_items_query = session.prepare("SELECT rid , numbers FROM required_item WHERE pid = ?;")
create_required_items_query = session.prepare(
    "INSERT INTO required_item (pid , rid , numbers ) VALUES ( ? , ? , ? ) ;")
delete_required_item_query = session.prepare("DELETE from required_item WHERE pid = ? ;")
delete_build_query = session.prepare("DELETE from product_builds WHERE pid = ? IF EXISTS")
insert_required_trash_query = session.prepare(
    "INSERT INTO required_trash (pid , rid , numbers ) VALUES ( ? , ? , ? ) ;")
get_required_trash_query = session.prepare("SELECT * FROM required_trash WHERE pid = ? ;")
delete_required_trash_query = session.prepare("DELETE FROM required_trash WHERE pid = ? ;")
get_req_items_by_rid_query = session.prepare("SELECT * FROM required_item_by_rid WHERE rid= ? ;")
insert_build_trash_query = session.prepare(
    "INSERT INTO product_builds_trash (pid , building , instock, needed , recommended ) VALUES ( ?,?,?,?,? ) ;")
get_building_query = session.prepare("SELECT building FROM product_builds WHERE pid = ? LIMIT 1;")
get_stock_query = session.prepare("SELECT instock FROM product_builds WHERE pid = ? LIMIT 1;")
update_build_query = session.prepare("UPDATE product_builds SET building = ?  WHERE pid = ? IF EXISTS ;")
update_stock_query = session.prepare("UPDATE product_builds SET instock = ?  WHERE pid = ? IF EXISTS ;")
restore_build_query = session.prepare("SELECT * FROM product_builds_trash WHERE pid = ? LIMIT 1;")
delete_build_trash_query = session.prepare("DELETE from product_builds_trash WHERE pid = ? IF EXISTS ;")
update_needed_query = session.prepare("UPDATE product_builds SET needed = ? WHERE pid = ?  IF EXISTS ;")
get_needed_query = session.prepare("SELECT needed FROM product_builds WHERE pid = ? LIMIT 1;")
update_complete_build_query = session.prepare(
    "UPDATE complete_build SET numbers = numbers + ?  WHERE date = ? AND pid = ? ;")


def create_build(pid, building=0, instock=0, needed=0, recommended=0):
    session.execute(create_build_query, (pid, building, instock, needed, recommended))


def get_builds():
    a = session.execute(get_builds_query)
    return a.all()


def get_build(pid):
    a = session.execute(get_build_query, (pid,)).one()
    if a is None:
        raise NotFound
    return a


def get_building(pid):
    a = session.execute(get_building_query, (pid,)).one()
    if not a:
        return 0
    return a.get('building')


def get_stock(pid):
    a = session.execute(get_stock_query, (pid,)).one()
    if not a:
        return 0
    return a.get('instock')


def delete_build(pid, moveto_trash=True):
    if moveto_trash:
        a = get_build(pid=pid)
        session.execute(insert_build_trash_query,
                        (pid, a.get('building'), a.get('instock'), a.get('needed'), a.get('recommended')))
    a = session.execute(delete_build_query, (pid,)).was_applied
    return a


def edit_building(pid, numbers):
    session.execute(update_build_query, (numbers, pid))


def build_product(pid, numbers=1):
    a = get_building(pid)
    numbers = a + numbers
    session.execute(update_build_query, (numbers, pid))


def discard_product(pid, numbers=1):
    a = get_build(pid)
    numbers = a.get('building') - numbers
    if numbers >= 0:
        session.execute(update_build_query, (numbers, pid))
    else:
        raise InvalidNumber


def edit_stock(pid, numbers):
    session.execute(update_stock_query, (numbers, pid))


def add_stock(pid, numbers):
    stock = get_stock(pid)
    building = get_building(pid)
    if numbers <= building:
        stock = stock + numbers
        session.execute(update_stock_query, (stock, pid))
        discard_product(pid, numbers)
        update_complete_build(pid, numbers)
        # generate_needed(pid)
        remove_needed_by_pid(pid, numbers)
    else:
        raise InvalidNumber


def discard_stock(pid, numbers):
    a = get_stock(pid)
    numbers = a - numbers
    if numbers >= 0:
        session.execute(update_stock_query, (numbers, pid))
    else:
        raise InvalidNumber


def get_required_items(pid):
    a = session.execute(get_req_items_query, (pid,))
    return a.all()


def create_required_item(pid, rid, numbers):
    return session.execute(create_required_items_query, (pid, rid, numbers))


def create_required_items(pid, rid, numbers):
    for r, n in zip(rid, numbers):
        # create_required_item(pid, r, n)
        session.execute_async(create_required_items_query, (pid, r, n))
        # print(numbers[i])
    # pass
    # print(pid, rid, numbers)


def create_required_items_by_data(data):
    for i in data:
        session.execute_async(create_required_items_query, (i.get('pid'), i.get('rid'), i.get('numbers')))


def create_required_trashes(pid, rid, numbers):
    for r, n in zip(rid, numbers):
        session.execute_async(insert_required_trash_query, (pid, r, n))


def delete_required_items(pid, moveto_trash=True):
    if moveto_trash:
        a = get_required_items(pid=pid)
        for i in a:
            session.execute_async(insert_required_trash_query, (pid, i.get('rid'), i.get('numbers')))
    session.execute(delete_required_item_query, (pid,))
    return


def get_required_trash(pid):
    a = session.execute(get_required_trash_query, (pid,)).all()
    # session.execute_async(delete_required_trash_query, (pid,))
    return a


def delete_required_trash(pid):
    session.execute_async(delete_required_trash_query, (pid,))


def get_req_items_by_rid(rid):
    a = session.execute(get_req_items_by_rid_query, (rid,)).all()
    return a


def get_max_builds(pid):
    r = get_required_items(pid)
    a = None
    for i in r:
        m = get_stock(i.get('rid')) // i.get('numbers')
        if a is None:
            a = m
        else:
            a = min(a, m)
    return a


def safe_build(pid, numbers):
    builds = get_max_builds(pid)

    if builds is None:
        builds = get_build(pid).get('building')
        build_product(pid, numbers)
        return numbers
        # print(a)
    if builds is not None and builds >= numbers:
        items = get_required_items(pid)
        for i in items:
            total = i.get('numbers') * numbers
            discard_stock(pid=i.get('rid'), numbers=total)
            add_needed(rid=i.get('rid'), numbers=total)
        build_product(pid, numbers)
        return numbers
    elif builds <= numbers:
        return builds - numbers


def safe_discard(pid, numbers):
    building = get_building(pid)
    if numbers <= building:
        items = get_required_items(pid)
        for i in items:
            total = i.get('numbers') * numbers
            add_stock(pid=i.get('rid'), numbers=total)
            remove_needed(rid=i.get('rid'), numbers=total)
        discard_product(pid, numbers)
        # print('valid to discard')
        return numbers
    else:
        return building - numbers


def restore_build_trash(pid):
    trash = session.execute(restore_build_query, (pid,)).one()
    session.execute(delete_build_trash_query, (pid,))
    create_build(**trash)
    print(trash)


def generate_needed(rid):
    req = get_req_items_by_rid(rid)
    needed = 0
    for i in req:
        building = get_building(pid=i.get('pid'))
        needed = needed + building * i.get('numbers')
    session.execute(update_needed_query, (needed, rid))
    return needed


def remove_needed_by_pid(pid, numbers):
    items = get_required_items(pid)
    for i in items:
        # print(i)
        remove_needed(i.get('rid'), i.get('numbers') * numbers)


def add_needed(rid, numbers):
    needed = get_needed(rid)
    needed = needed + numbers
    return update_needed(rid, needed)


def remove_needed(rid, numbers):
    needed = get_needed(rid)
    if needed >= numbers:
        needed = needed - numbers
        return update_needed(rid, needed)
    return False


def update_needed(rid, needed=0):
    return session.execute(update_needed_query, (needed, rid)).was_applied


def get_needed(rid):
    needed = session.execute(get_needed_query, (rid,)).one()
    if needed:
        return needed.get('needed')
    return 0


def update_complete_build(pid, numbers, date=None, ):
    if date is None:
        date = dates.today()
    else:
        date = dates.fromtimestamp(date)
    session.execute(update_complete_build_query, (numbers, date, pid))


# for testing the query's
if __name__ == '__main__':
    # print(get_build(uuid.UUID('b11c39cf-0ced-45ed-88d4-015b9a3d4cfe')))
    # print(get_required_items(uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053')))
    # print(create_required_item(pid=uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053'),
    #                              rid=uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053'), numbers=233))
    # a = get_required_items(pid=uuid.UUID('3bc4555a-9b02-11ed-91a5-f889d2e645af'))
    # for i in a:
    #     print(i['numbers'])
    # a = get_required_trash(uuid.UUID('ee0f9394-9bb8-11ed-b7ed-f889d2e645af'))
    # create_required_items(data=a)
    # create_build(uuid.UUID('1e24dc30-526b-4998-8bf6-671fba9536aa'), instock=12)
    # a = get_build(pid=uuid.UUID('2e24dc30-526b-4998-8bf6-671fba9536aa'))
    # print(a['pid'])
    # build_product(uuid.UUID('c8147014-9cc7-11ed-9a52-f889d2e645af'))
    # print(get_build(uuid.UUID('c8147014-9cc7-11ed-9a52-f889d2e645af')))
    # print(get_building(uuid.UUID('c8147014-9cc7-11ed-9a52-f889d2e645af')))
    # add_stock(pid=uuid.UUID('5081a726-9ed2-11ed-8b52-f889d2e645af'), numbers=212)
    # print(get_build(uuid.UUID('5081a726-9ed2-11ed-8b52-f889d2e645af')))
    # print(get_max_builds(uuid.UUID('cb27fb90-9f1a-11ed-801a-f889d2e645af')))
    # maxbuilds = get_max_builds(uuid.UUID('cb27fb90-9f1a-11ed-801a-f889d2e645af'))
    # safe_build(uuid.UUID('cb27fb90-9f1a-11ed-801a-f889d2e645af'), numbers=4)
    # safe_discard(uuid.UUID('cb27fb90-9f1a-11ed-801a-f889d2e645af'), numbers=1)
    # restore_build_trash(uuid.UUID('1e0f9f3b-14bb-4bf2-afa2-79feaa0c71e6'))
    # print(update_needed(uuid.UUID('89eb8424-a250-11ed-a23b-f889d2e641af')))
    # print(get_needed(uuid.UUID('89eb8424-a250-11ed-a23b-f889d2e645af')))
    # print(generate_needed(uuid.UUID('89eb8424-a250-11ed-a23b-f889d2e645af')))
    # remove_needed(uuid.UUID('89eb8424-a250-11ed-a23b-f889d2e645af'), numbers=12)
    # remove_needed_by_pid(uuid.UUID('dca8a65a-a490-11ed-9017-f889d2e645af'), 12)
    update_complete_build(pid=uuid.UUID('154f1934-a4b5-11ed-ad91-f889d2e645af'), date=167558445)
