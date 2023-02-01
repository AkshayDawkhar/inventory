from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
import uuid
# from .reqitem_serializer import RequiredItems
from build_API.cqlqueries import BuildCQL

b = BuildCQL()


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


class ProductCQL:
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('model1')
    session.row_factory = dict_factory
    m = ['media1', 'media player dj200usb pinto', 'media']
    get_product_query = session.prepare("SELECT * FROM product_list1_by_id WHERE pid = ? LIMIT  1 ")
    get_pid_query = session.prepare(
        "SELECT pid FROM product_list1 WHERE pname = ? AND color= ? AND required_items = ? ;")
    create_product_query = session.prepare(
        "INSERT INTO product_list1 ( pname , required_items , color , category , dname , pid ) VALUES ( ?, ?,?, ?, ?, ?) IF NOT EXISTS ;")
    create_by_id_query = session.prepare(
        "INSERT INTO product_list1_by_id (pid , required_items , pname , color ,dname , category  ) VALUES (?,?,?,?,?,? );")
    update_by_id_query = session.prepare(
        "UPDATE product_list1_by_id SET pname = ?, required_items =?, color = ?, category = ?, dname = ? WHERE pid = ? IF EXISTS;")
    delete_product_query = session.prepare(
        "DELETE FROM product_list1 WHERE pname =? AND required_items =? AND color = ? IF EXISTS;")
    delete_product_by_id_query = session.prepare(
        "DELETE FROM product_list1_by_id WHERE pid =? IF EXISTS ;")
    insert_into_trash_query = session.prepare(
        "INSERT INTO trash (pname , required_items , color , category , dname , pid ) VALUES ( ?,?,?, ?, ?, ? ) USING TTL 2592000;")
    restore_fromTrash_query = session.prepare("SELECT * from trash WHERE pid = ? LIMIT 1;")
    delete_Trash_query = session.prepare("DELETE from trash WHERE pid = ? IF EXISTS;")
    get_trashes_query = session.prepare("SELECT dname,pid,TTL(dname) FROM trash ;")
    product_list_query = session.prepare("SELECT dname , pid FROM product_list1 ;")
    get_trash_query = session.prepare(
        "SELECT pid,dname,pname,color,required_items,category,TTL(pname) FROM trash WHERE pid = ? ;")

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

    def create_product(self, pname, required_items, color, category, dname, required_items_no=None, pid=None):
        if not pid:
            pid = uuid.uuid1()
            b.create_build(pid=pid)
        r = self.session.execute(self.create_product_query, (pname, set(required_items), color, category, dname, pid))
        if r.one()['[applied]']:
            r1 = self.session.execute(self.create_by_id_query,
                                      (pid, set(required_items), pname, color, dname, category,))
            # b.create_build(pid=pid)
            if required_items_no is not None:
                b.create_required_items(pid=pid, rid=set(required_items), numbers=required_items_no)
            else:
                pass
        return r.one()

    def delete_product(self, pid=None, pname=None, required_items=None, color=None, moveto_trash=True,
                       removefrom_product_list1=True,
                       removefrom_product_list1_by_id=True):
        if moveto_trash:
            it = self.get_product(pid)
            # INSERT INTO trash_product_list1 (pname , required_items , color , category , dname , pid ) VALUES ( '1',{'row1'},'red', '12', 'AS', UUID() ) ;
            self.session.execute(self.insert_into_trash_query, (
                it['pname'], it['required_items'], it['color'], it['category'], it['dname'], it['pid']))
            b.delete_build(pid=pid, moveto_trash=moveto_trash)

        if removefrom_product_list1_by_id:
            if pname is None:
                av = self.get_product(pid)
                pname = av['pname']
                required_items = av['required_items']
                color = av['color']
            a = self.session.execute(self.delete_product_by_id_query, (pid,))
            b.delete_required_items(pid=pid, moveto_trash=moveto_trash)
            # return a
        if removefrom_product_list1:
            a1 = self.session.execute(self.delete_product_query, (pname, set(required_items), color))
        return a1.one()['[applied]']

    def update_product(self, pid, pname, color, required_items, dname, category, required_items_no):

        gt = self.get_product(pid)
        required_items = set([uuid.UUID(r) for r in required_items])
        try:
            gt1 = self.get_pid(pname, color, required_items)
            if pid != gt1:
                raise Conflict
        except NotFound:
            pass
        a = self.session.execute(self.update_by_id_query, (pname, set(required_items), color, category, dname, pid))
        # FOR deleting the product from product_list1 calling delete product
        tf = self.delete_product(moveto_trash=False, removefrom_product_list1_by_id=False, pname=gt['pname'],
                                 required_items=gt['required_items'], color=gt['color'])
        gtt = self.session.execute(self.create_product_query, (pname, set(required_items), color, category, dname, pid))
        b.delete_required_items(pid=pid, moveto_trash=False)
        b.create_required_items(pid=pid, rid=required_items, numbers=required_items_no)
        return gtt.one()

    # Trash product
    def get_trashes(self):
        return self.session.execute(self.get_trashes_query).all()

    def restore(self, pid):
        a = self.session.execute(self.restore_fromTrash_query, (pid,)).one()
        ra = b.get_required_trash(pid=pid)
        # self.session.execute(self.delete_Trash_query, (pid,))
        # self.create_product(pname=a['pname'],required_items=a['required_items'],color=a['color'],category=a['category'])
        if a is not None:
            try:
                self.get_pid(pname=a['pname'], color=a['color'], required_items=a['required_items'])
                raise Conflict
            except NotFound:
                self.session.execute(self.delete_Trash_query, (pid,))
                b.delete_required_trash(pid=pid)
                b.create_required_items_by_data(data=ra)
                self.create_product(**a)
        else:
            raise DatabaseError

    def delete_trash(self, pid):
        a = self.session.execute(self.delete_Trash_query, (pid,)).one()['[applied]']
        return a

    def get_trash(self, pid):
        a = self.session.execute(self.get_trash_query, (pid,)).one()
        if a is None:
            raise NotFound
        a['required_items'] = list(a['required_items'])
        return a


if __name__ == "__main__":
    p = ProductCQL()
    # a = p.get_product(uuid.UUID('f49b3ac8-965f-11ed-958e-f889d2e645af'))
    # print(a)
    # INSERT INTO trash_product_list1 (pname , required_items , color , category , dname , pid ) VALUES ( '1',{'row1'},'red', '12', 'AS', UUID() ) ;
    # p.session.execute(p.insert_into_trash_query,
    #                   ('1', ['row1'], 'red', '12', 'AS12', uuid.UUID('f49b3ac8-965f-11ed-958e-f889d2e645af')))
    # # print(p.prduct_list())
    # s = RequiredItems(data=['9fac422c-942b-11ed-a23f-f889d2e645af'])
    l = ['9fac422c-942b-11ed-a23f-f889d2e645af', '9fac422c-942b-11ed-a23f-f889d2e646af',
         '1fac422c-942b-11ed-a23f-f889d2e645af']
    print(p.get_pid('media', 'red', [uuid.UUID(uid) for uid in l]))
    # print(p.create_product('media4', ['row1', 'row2', 'row3', 'row5'], 'black', 'category', 'dname'))
    # print(p.update_product(pid=uuid.UUID('9fac422c-942b-11ed-a23f-f889d2e645af'), pname='sounds', color='black',
    #                        required_items=['row2', 'row2'], dname='sounds', category='soundss'))
    # print(p.delete_product(moveto_trash=False, removefrom_product_list1_by_id=False, pname='djchesounds',
    #                        required_items=['row1'], color='black'))
    # print(p.update_product(pid=uuid.UUID('757e0bb6-948f-11ed-900f-f889d2e645af'), pname='m4soound', color='redd',
    #                        required_items=['ROW2'], dname='M4-soound', category='pink
    # p.restore(pid=uuid.UUID('ba4c8576-968b-11ed-8e04-f889d2e645af'))
    # print(p.delete_trash(pid=uuid.UUID('ba4c8576-968b-11ed-8e04-f889d2e645af')))
    # print(p.get_trash(uuid.UUID('49ca02c8-9745-11ed-8318-f889d2e645af')))
