from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
import uuid

class BuildCQL:
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('model1')
    session.row_factory = dict_factory

    def get_builds(self):
        pass

    def get_build(self, pid):
        p = self.session.prepare("SELECT * FROM product_builds ;")
        a = self.session.execute(p)
        return a.all()


if __name__ == '__main__':
    b = BuildCQL()
    print(b.get_build(uuid.UUID('b11c39cf-0ced-45ed-88d4-015b9a3d4cfe')))
