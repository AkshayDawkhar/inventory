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


class InvalidDictionary(DatabaseError):
    pass


class ProductCQL:
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.row_factory = dict_factory
    m = ['media1', 'media player dj200usb pinto', 'media']
    get_product_query = session.prepare("SELECT * FROM model1.product_list1_by_id WHERE pid = ? LIMIT  1 ")

    def get_product(self, pid):
        a = self.session.execute(self.get_product_query, (pid,))
        if not a:
            raise NotFound("Product Not Found %s" % (pid,))

        a.one()['required_iteams'] = list(a.one()['required_iteams'])
        return a.one()

    def product_list(self):
        sp = self.session.prepare("SELECT dname , pid FROM model1.product_list1 WHERE pname = ?")
        a = self.session.execute("SELECT dname , pid FROM model1.product_list1 ;")
        return a.all()


if __name__ == "__main__":
    p = ProductCQL()
    print(p.get_product(uuid.UUID('6555aec7-df75-4da4-b2a6-1c18907ff18b')))
    # print(p.prduct_list())
