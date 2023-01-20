from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
import uuid


class BuildCQL:
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('model1')
    session.row_factory = dict_factory
    get_builds_query = session.prepare("SELECT * FROM product_builds ;")
    get_build_query = session.prepare("SELECT * FROM product_builds WHERE pid = ? LIMIT 1;")

    def get_builds(self):
        a = self.session.execute(self.get_builds_query)
        return a.all()

    def get_build(self, pid):
        a = self.session.execute(self.get_build_query, (pid,))
        return a.one()


# for testing the query's
if __name__ == '__main__':
    b = BuildCQL()
    print(b.get_build(uuid.UUID('b11c39cf-0ced-45ed-88d4-015b9a3d4cfe')))
