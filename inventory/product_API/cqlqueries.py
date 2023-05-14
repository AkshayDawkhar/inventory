from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
import uuid
# from .reqitem_serializer import RequiredItems
import build_API.cqlqueries as build_cql


# build_cql = BuildCQL()


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
product_category_query = session.prepare("SELECT dname,pid FROM product_list1 WHERE category = ? ALLOW FILTERING ;")
get_trash_query = session.prepare(
    "SELECT pid,dname,pname,color,required_items,category,TTL(pname) FROM trash WHERE pid = ? ;")


def get_product(pid):
    a = session.execute(get_product_query, (pid,)).one()
    if not a:
        raise NotFound("Product Not Found %s" % (pid,))

    a['required_items'] = list(a.get('required_items'))
    return a


def product_list(category):
    if category is not None:
        # print('------------->category')

        a = list(session.execute(product_category_query,(category,)).all())
        return a
    # sp = session.prepare("SELECT dname , pid FROM product_list1 WHERE pname = ?")
    return session.execute(product_list_query).all()
    # return a.all()


def get_pid(pname, color, required_items):
    r = session.execute(get_pid_query, (pname, color, set(required_items))).one()
    if not r:
        raise NotFound('product not found')
    return r.get('pid')


def create_product(pname, required_items, color, category, dname, required_items_no=None, pid=None):
    if not pid:
        pid = uuid.uuid1()
        build_cql.create_build(pid=pid)
    r = session.execute(create_product_query, (pname, set(required_items), color, category, dname, pid))
    if r.was_applied:
        r1 = session.execute(create_by_id_query,
                             (pid, set(required_items), pname, color, dname, category,))
        # build_cql.create_build(pid=pid)
        if required_items_no is not None:
            build_cql.create_required_items(pid=pid, rid=set(required_items), numbers=required_items_no)
        else:
            pass
    return r.one()


def delete_product(pid=None, pname=None, required_items=None, color=None, moveto_trash=True,
                   removefrom_product_list1=True,
                   removefrom_product_list1_by_id=True):
    if moveto_trash:
        it = get_product(pid)
        # INSERT INTO trash_product_list1 (pname , required_items , color , category , dname , pid ) VALUES ( '1',{'row1'},'red', '12', 'AS', UUID() ) ;
        session.execute(insert_into_trash_query, (
            it.get('pname'), it.get('required_items'), it.get('color'), it.get('category'), it.get('dname'), it.get('pid')))
        build_cql.delete_build(pid=pid, moveto_trash=moveto_trash)

    if removefrom_product_list1_by_id:
        if pname is None:
            av = get_product(pid)
            pname = av.get('pname')
            required_items = av.get('required_items')
            color = av.get('color')
        a = session.execute(delete_product_by_id_query, (pid,))
        build_cql.delete_required_items(pid=pid, moveto_trash=moveto_trash)
        # return a
    if removefrom_product_list1:
        a1 = session.execute(delete_product_query, (pname, set(required_items), color))
    return a1.was_applied


def update_product(pid, pname, color, required_items, dname, category, required_items_no):
    gt = get_product(pid)
    required_items = set([uuid.UUID(r) for r in required_items])
    try:
        gt1 = get_pid(pname, color, required_items)
        if pid != gt1:
            raise Conflict
    except NotFound:
        pass
    a = session.execute(update_by_id_query, (pname, set(required_items), color, category, dname, pid))
    # FOR deleting the product from product_list1 calling delete product
    tf = delete_product(moveto_trash=False, removefrom_product_list1_by_id=False, pname=gt.get('pname'),
                        required_items=gt.get('required_items'), color=gt.get('color'))
    gtt = session.execute(create_product_query, (pname, set(required_items), color, category, dname, pid))
    build_cql.delete_required_items(pid=pid, moveto_trash=False)
    build_cql.create_required_items(pid=pid, rid=required_items, numbers=required_items_no)
    return gtt.one()


# Trash product
def get_trashes():
    return session.execute(get_trashes_query).all()


def restore(pid):
    a = session.execute(restore_fromTrash_query, (pid,)).one()
    ra = build_cql.get_required_trash(pid=pid)
    # session.execute(delete_Trash_query, (pid,))
    # create_product(pname=a.get('pname'),required_items=a.get('required_items'),color=a.get('color'),category=a.get('category'))
    if a is not None:
        try:
            get_pid(pname=a.get('pname'), color=a.get('color'), required_items=a.get('required_items'))
            raise Conflict
        except NotFound:
            session.execute(delete_Trash_query, (pid,))
            build_cql.delete_required_trash(pid=pid)
            build_cql.create_required_items_by_data(data=ra)
            build_cql.restore_build_trash(pid=pid)
            create_product(**a)
    else:
        raise DatabaseError


def delete_trash(pid):
    return session.execute(delete_Trash_query, (pid,)).was_applied


def get_trash(pid):
    a = session.execute(get_trash_query, (pid,)).one()
    if a is None:
        raise NotFound
    a['required_items'] = list(a.get('required_items'))
    return a


if __name__ == "__main__":
    # p = ProductCQL()
    # a = p.get_product(uuid.UUID('f49b3ac8-965f-11ed-958e-f889d2e645af'))
    # print(a)
    # INSERT INTO trash_product_list1 (pname , required_items , color , category , dname , pid ) VALUES ( '1',{'row1'},'red', '12', 'AS', UUID() ) ;
    # p.session.execute(p.insert_into_trash_query,
    #                   ('1', ['row1'], 'red', '12', 'AS12', uuid.UUID('f49b3ac8-965f-11ed-958e-f889d2e645af')))
    # # print(p.prduct_list())
    # s = RequiredItems(data=['9fac422c-942b-11ed-a23f-f889d2e645af'])
    l = ['9fac422c-942b-11ed-a23f-f889d2e645af', '9fac422c-942b-11ed-a23f-f889d2e646af',
         '1fac422c-942b-11ed-a23f-f889d2e645af']
    print(get_pid('media', 'red', [uuid.UUID(uid) for uid in l]))
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
