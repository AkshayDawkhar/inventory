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


class BuildCQL:
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
    update_build = session.prepare("UPDATE product_builds SET building = ?  WHERE pid = ?;")

    def create_build(self, pid, building=0, instock=0, needed=0, recommended=0):
        self.session.execute(self.create_build_query, (pid, building, instock, needed, recommended))

    def get_builds(self):
        a = self.session.execute(self.get_builds_query)
        return a.all()

    def get_build(self, pid):
        a = self.session.execute(self.get_build_query, (pid,)).one()
        if a is None:
            raise NotFound
        return a

    def delete_build(self, pid, moveto_trash=True):
        if moveto_trash:
            a = self.get_build(pid=pid)
            self.session.execute(self.insert_build_trash_query,
                                 (pid, a['building'], a['instock'], a['needed'], a['recommended']))
        a = self.session.execute(self.delete_build_query, (pid,)).one()['[applied]']
        return a

    def build_product(self, pid, numbers=1):
        a = self.get_build(pid)
        numbers = a['building'] + numbers
        self.session.execute(self.update_build, (numbers, pid))
        # self.create_build(pid=pid, building=a['building'] + 1, instock=a['instock'], needed=a['needed'], recommended=0)

    def discard_product(self, pid, numbers=1):
        a = self.get_build(pid)
        numbers = a['building'] - numbers
        if numbers >= 0:
            self.session.execute(self.update_build, (numbers, pid))
        else:
            raise InvalidNumber

    def get_required_items(self, pid):
        a = self.session.execute(self.get_req_items_query, (pid,))
        return a.all()

    def create_required_item(self, pid, rid, numbers):
        a = self.session.execute(self.create_required_items_query, (pid, rid, numbers))
        return a

    def create_required_items(self, pid, rid, numbers):
        for r, n in zip(rid, numbers):
            # self.create_required_item(pid, r, n)
            self.session.execute_async(self.create_required_items_query, (pid, r, n))
            # print(numbers[i])
        # pass
        # print(pid, rid, numbers)

    def create_required_items_by_data(self, data):
        for i in data:
            self.session.execute_async(self.create_required_items_query, (i['pid'], i['rid'], i['numbers']))

    def create_required_trashes(self, pid, rid, numbers):
        for r, n in zip(rid, numbers):
            self.session.execute_async(self.insert_required_trash_query, (pid, r, n))

    def delete_required_items(self, pid, moveto_trash=True):
        if moveto_trash:
            a = self.get_required_items(pid=pid)
            for i in a:
                self.session.execute_async(self.insert_required_trash_query, (pid, i['rid'], i['numbers']))
        self.session.execute(self.delete_required_item_query, (pid,))
        return

    def get_required_trash(self, pid):
        a = self.session.execute(self.get_required_trash_query, (pid,)).all()
        # self.session.execute_async(self.delete_required_trash_query, (pid,))
        return a

    def delete_required_trash(self, pid):
        self.session.execute_async(self.delete_required_trash_query, (pid,))

    def get_req_items_by_rid(self, rid):
        a = self.session.execute(self.get_req_items_by_rid_query, (rid,)).all()
        return a


# for testing the query's
if __name__ == '__main__':
    b = BuildCQL()
    # print(b.get_build(uuid.UUID('b11c39cf-0ced-45ed-88d4-015b9a3d4cfe')))
    # print(b.get_required_items(uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053')))
    # print(b.create_required_item(pid=uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053'),
    #                              rid=uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053'), numbers=233))
    # a = b.get_required_items(pid=uuid.UUID('3bc4555a-9b02-11ed-91a5-f889d2e645af'))
    # for i in a:
    #     print(i['numbers'])
    # a = b.get_required_trash(uuid.UUID('ee0f9394-9bb8-11ed-b7ed-f889d2e645af'))
    # b.create_required_items(data=a)
    # b.create_build(uuid.UUID('1e24dc30-526b-4998-8bf6-671fba9536aa'), instock=12)
    # a = b.get_build(pid=uuid.UUID('2e24dc30-526b-4998-8bf6-671fba9536aa'))
    # print(a['pid'])
    b.build_product(uuid.UUID('c8147014-9cc7-11ed-9a52-f889d2e645af'))
    print(b.get_build(uuid.UUID('c8147014-9cc7-11ed-9a52-f889d2e645af')))
