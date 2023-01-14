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
    session = cluster.connect('model1')
    session.row_factory = dict_factory
    m = ['media1', 'media player dj200usb pinto', 'media']
    get_product_query = session.prepare("SELECT * FROM product_list1_by_id WHERE pid = ? LIMIT  1 ")
    get_pid_query = session.prepare("SELECT pid FROM product_list1 WHERE pname = ? AND color= ? AND required_items = ? ;")
    create_product_query = session.prepare("INSERT INTO product_list1 ( pname , required_items , color , category , dname , pid ) VALUES ( ?, ?,?, ?, ?, ?) IF NOT EXISTS ;")
    create_by_id_query = session.prepare("INSERT INTO product_list1_by_id (pid , required_items , pname , color ,dname , category  ) VALUES (?,?,?,?,?,? );")
    update_by_id_query = session.prepare("UPDATE product_list1_by_id SET pname = ?, required_items =?, color = ?, category = ?, dname = ? WHERE pid = ? IF EXISTS;")
    delete_product_query = session.prepare("DELETE FROM product_list1 WHERE pname =? AND required_items =? AND color = ? IF EXISTS;")
    product_list_query = session.prepare("SELECT dname , pid FROM product_list1 ;")
    def get_product(self, pid):
        a = self.session.execute(self.get_product_query, (pid,))
        if not a:
            raise NotFound("Product Not Found %s" % (pid,))

        a.one()['required_items'] = list(a.one()['required_items'])
        return a.one()

    def product_list(self):
        # sp = self.session.prepare("SELECT dname , pid FROM product_list1 WHERE pname = ?")
        a = self.session.execute(self.product_list_query)
        return a.all()

    def get_pid(self, pname, color, required_items):
        r = self.session.execute(self.get_pid_query, (pname, color, set(required_items)))
        if not r.one():
            raise NotFound('product not found')
        return r.one()['pid']

    def create_product(self, pname, required_items, color, category, dname, pid=None):
        if not pid: pid = uuid.uuid1()
        r = self.session.execute(self.create_product_query, (pname, set(required_items), color, category, dname, pid))
        if r.one()['[applied]']:
            r1 = self.session.execute(self.create_by_id_query, (pid, set(required_items), pname, color, dname, category,))
        return r.one()

    def delete_product(self, pname, required_items, color, moveto_trash=True, removefrom_product_list1=True,
                       removefrom_product_list1_by_id=True):
        if moveto_trash:
            pass
        else:
            if removefrom_product_list1_by_id:
                pass
            if removefrom_product_list1:
                a1 = self.session.execute(self.delete_product_query, (pname, set(required_items), color))
        return a1.one()['[applied]']

    def update_product(self, pid, pname, color, required_items, dname, category):

        gt = self.get_product(pid)
        a = self.session.execute(self.update_by_id_query, (pname, required_items, color, category, dname, pid))
        # FOR deleting the product from product_list1 calling delete product
        tf = self.delete_product(moveto_trash=False, removefrom_product_list1_by_id=False, pname=pname,
                                 required_items=required_items, color=color)
        # if tf:

        return gt


if __name__ == "__main__":
    p = ProductCQL()
    # print(p.get_product(uuid.UUID('6555aec7-df75-4da4-b2a6-1c18907ff18b')))
    # print(p.prduct_list())
    # print(p.get_pid('media', 'red', ['row1', 'row2', 'row4', 'row3']))
    # print(p.create_product('media4', ['row1', 'row2', 'row3', 'row5'], 'black', 'category', 'dname'))
    # print(p.update_product(pid=uuid.UUID('9fac422c-942b-11ed-a23f-f889d2e645af'), pname='sounds', color='black',
    #                        required_items=['row2', 'row2'], dname='sounds', category='soundss'))
    print(p.delete_product(moveto_trash=False, removefrom_product_list1_by_id=False, pname='djchesounds',
                           required_items=['row1'], color='black'))