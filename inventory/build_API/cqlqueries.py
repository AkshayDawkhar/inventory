from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
import uuid


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


class BuildCQL:
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('model1')
    session.row_factory = dict_factory
    get_builds_query = session.prepare("SELECT * FROM product_builds ;")
    get_build_query = session.prepare("SELECT * FROM product_builds WHERE pid = ? LIMIT 1;")
    get_req_items_query = session.prepare("SELECT rid , numbers FROM required_item WHERE pid = ?;")
    create_required_items_query = session.prepare(
        "INSERT INTO required_item (pid , rid , numbers ) VALUES ( ? , ? , ? ) ;")
    delete_required_item_query = session.prepare("DELETE from required_item WHERE pid = ? ;")
    delete_build_query = session.prepare("DELETE from product_builds WHERE pid = ? IF EXISTS")

    def get_builds(self):
        a = self.session.execute(self.get_builds_query)
        return a.all()

    def get_build(self, pid):
        a = self.session.execute(self.get_build_query, (pid,)).one()
        if a is None:
            raise NotFound
        return a

    def delete_build(self, pid):
        a = self.session.execute(self.delete_build_query, (pid,)).one()['[applied]']
        return a

    def get_required_items(self, pid):
        a = self.session.execute(self.get_req_items_query, (pid,))
        return a.all()

    def create_required_items(self, pid, rid, numbers):
        a = self.session.execute(self.create_required_items_query, (pid, rid, numbers))
        return a

    def delete_required_items(self, pid):
        self.session.execute(self.delete_required_item_query, (pid,))
        return


# for testing the query's
if __name__ == '__main__':
    b = BuildCQL()
    # print(b.get_build(uuid.UUID('b11c39cf-0ced-45ed-88d4-015b9a3d4cfe')))
    # print(b.get_required_items(uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053')))
    print(b.create_required_items(pid=uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053'),
                                  rid=uuid.UUID('8ecf1e8e-67f1-4338-bdb9-705887f22053'), numbers=233))
