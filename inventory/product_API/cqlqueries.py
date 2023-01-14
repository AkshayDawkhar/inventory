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

    def get_product(self, pid):
        a = self.session.execute(self.get_product_query, (pid,))
        if not a:
            raise NotFound("Product Not Found %s" % (pid,))

        a.one()['required_iteams'] = list(a.one()['required_iteams'])
        return a.one()

    def product_list(self):
        sp = self.session.prepare("SELECT dname , pid FROM product_list1 WHERE pname = ?")
        a = self.session.execute("SELECT dname , pid FROM product_list1 ;")
        return a.all()

    def get_pid(self, pname, color, required_iteams):
        sp = self.session.prepare(
            "SELECT pid FROM product_list1 WHERE pname = ? AND color= ? AND required_iteams = ? ;")
        r = self.session.execute(sp, (pname, color, set(required_iteams)))
        if not r.one():
            raise NotFound('product not found')
        return r.one()['pid']

    def create_product(self, pname, required_iteams, color, category, dname,pid=uuid.uuid1()):
        sp = self.session.prepare("INSERT INTO product_list1 ( pname , required_iteams , color , category , dname , "
                                  "pid ) VALUES ( ?, ?,?, ?, ?, ?) IF NOT EXISTS ;")
        sp1 = self.session.prepare("INSERT INTO product_list1_by_id (pid , required_iteams , pname , color ,dname ,  "
                                   "category  ) VALUES (?,?,?,?,?,? );")
        # pid = uuid.uuid1()
        r = self.session.execute(sp, (pname, set(required_iteams), color, category, dname, pid))
        if r.one()['[applied]']:
            r1 = self.session.execute(sp1, (pid, set(required_iteams), pname, color, dname, category,))
        return r.one()

    def delete_product(self,  pname, required_iteams, color,moveto_trash=True,removefrom_product_list1=True,removefrom_product_list1_by_id=True):
        if moveto_trash:
            pass
        else:
            if removefrom_product_list1_by_id:
                pass
            if removefrom_product_list1:
                sp1 = self.session.prepare("DELETE FROM product_list1 WHERE pname =? AND required_iteams =? AND color "
                                           "= ? IF EXISTS;")
                a1 = self.session.execute(sp1, (pname, set(required_iteams), color))
        return a1.one()['[applied]']

    def update_product(self, pid, pname, color, required_iteams, dname, category):

        sp = self.session.prepare("UPDATE product_list1_by_id SET pname = ?, required_iteams =?, color = ?, "
                                  "category = ?, dname = ? WHERE pid = ? IF EXISTS;")
        gt = self.get_product(pid)
        a = self.session.execute(sp, (pname, required_iteams, color, category, dname, pid))
        # FOR deleting the product from product_list1 calling delete product
        tf = self.delete_product(moveto_trash=False, removefrom_product_list1_by_id=False, pname=pname,
                           required_iteams=required_iteams, color=color)
        # if tf:

        return gt


if __name__ == "__main__":
    p = ProductCQL()
    # print(p.get_product(uuid.UUID('6555aec7-df75-4da4-b2a6-1c18907ff18b')))
    # print(p.prduct_list())
    # print(p.get_pid('media', 'red', ['row1', 'row2', 'row4', 'row3']))
    # print(p.create_product('media4', ['row1', 'row2', 'row3', 'row5'], 'black', 'category', 'dname'))
    # print(p.update_product(pid=uuid.UUID('9fac422c-942b-11ed-a23f-f889d2e645af'), pname='sounds', color='black',
    #                        required_iteams=['row2', 'row2'], dname='sounds', category='soundss'))
    print(p.delete_product(moveto_trash=False, removefrom_product_list1_by_id=False, pname='djchesounds',
                           required_iteams=['row1'], color='black'))
