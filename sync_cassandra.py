import os
from cassandra.cluster import Cluster
from django.core.management.base import BaseCommand

def test_cassandra():
    # for a -->  UserWarning: CQLENG_ALLOW_SCHEMA_MANAGEMENT environment variable is not set. Future versions of this
    # package will require this variable to enable management functions.
    if os.getenv('CQLENG_ALLOW_SCHEMA_MANAGEMENT') is None:
        os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    print('Connected to the db')
    # session.execute("CREATE TABLE IF NOT EXISTS  model1.product_list1 ( pname text ,color text , category text , dname text ,pid uuid , required_iteams frozen<set <text >> ,PRIMARY KEY (pname , required_iteams, color  )) WITH CLUSTERING ORDER BY (required_iteams ASC ) ;")
    rows = session.execute(
        "SELECT * FROM system_schema.keyspaces WHERE keyspace_name='model1'")

    if rows:
        a = input('model1 already exists did you want to delete it [yes/no]:')
        if a == 'yes':
            session.execute(" DROP KEYSPACE IF EXISTS model1 ;")
        else:
            return
    session.execute("CREATE KEYSPACE model1 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 } ;")
    session = cluster.connect('model1') 
    session.execute("CREATE TABLE IF NOT EXISTS  model1.product_list1 ( pname text ,color text , category text , dname text ,pid uuid , required_items frozen<set <uuid >> ,PRIMARY KEY (pname , required_items, color  )) WITH CLUSTERING ORDER BY (required_items ASC ) ;")
    session.execute("CREATE TABLE model1.product_list1_by_id (pid uuid PRIMARY KEY, category text, color text, dname text, pname text, required_items frozen<set<uuid >> );")
    session.execute("CREATE TABLE model1.trash (pid uuid PRIMARY KEY, category text, color text, dname text, pname text, required_items frozen<set<uuid >> );")
    session.execute("CREATE TABLE model1.required_item (pid uuid,rid uuid,numbers int,PRIMARY KEY (pid, rid))")
    session.execute("CREATE TABLE model1.product_builds (pid uuid PRIMARY KEY,building int,instock int,needed int,recommended int)")
    session.execute("CREATE MATERIALIZED VIEW required_item_by_rid AS SELECT * FROM model1.required_item WHERE pid IS NOT NULL AND rid IS NOT NULL PRIMARY KEY ( rid , pid ) ;")
    session.execute("CREATE TABLE model1.required_trash (pid uuid,rid uuid,numbers int,PRIMARY KEY (pid, rid))")
    session.execute("CREATE TABLE model1.product_builds_trash (pid uuid PRIMARY KEY,building int,instock int,needed int,recommended int);")
    session.execute("CREATE TABLE model1.orders (date date, pid uuid, numbers int, timestamp timestamp, PRIMARY KEY (date, pid))")
    session.execute("CREATE MATERIALIZED VIEW orders_by_pid AS SELECT * FROM orders WHERE pid IS NOT NULL AND date IS NOT NULL  AND numbers IS NOT NULL and timestamp IS NOT NULL PRIMARY KEY ( pid ,date) ;")
    session.execute("CREATE TABLE complete_order ( date date ,pid uuid , number counter,PRIMARY KEY (date , pid)) ;")
    session.execute("CREATE TABLE complete_build ( date date ,pid uuid , numbers counter ,PRIMARY KEY (date , pid)) ;")
    session.execute("CREATE TABLE user_worker ( mail text ,username text , fname text , lname text ,password text , PRIMARY KEY (username)) ;")
    session.execute("CREATE TABLE user_admin ( mail text  ,username text , fname text , lname text ,password text , PRIMARY KEY (username)) ;")
    session.execute("CREATE TABLE reg_mail_worker (mail text PRIMARY KEY ) ;")
    session.execute_async("CREATE TABLE reg_mail_admin (mail text PRIMARY KEY ) ;")
    print('done')
    # con = connection.register_connection('cluster', session=sec)
    # create_keyspace_simple('model1', 1, connections=['cluster'])
    # print('synchronizing db ')
    # sync_table(ProductList)
    # mc = ProductList(pname='a', dname='A', required_items=['a', 'b'], category='mic', pid=uuid.uuid1())
    # mc.save()
if __name__ == "__main__":
    test_cassandra()
