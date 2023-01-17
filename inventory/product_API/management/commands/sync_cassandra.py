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
        session.execute(" DROP KEYSPACE IF EXISTS model1 ;")
    session.execute("CREATE KEYSPACE model1 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 } ;")
    session.execute("CREATE TABLE IF NOT EXISTS  model1.product_list1 ( pname text ,color text , category text , dname text ,pid uuid , required_items frozen<set <text >> ,PRIMARY KEY (pname , required_items, color  )) WITH CLUSTERING ORDER BY (required_items ASC ) ;")
    session.execute("CREATE TABLE IF NOT EXISTS model1.product_list1_by_id (pid uuid PRIMARY KEY,category text,color text,dname text,pname text,required_items frozen<set<text>>)")
    print('done')
    # con = connection.register_connection('cluster', session=sec)
    # create_keyspace_simple('model1', 1, connections=['cluster'])
    # print('synchronizing db ')
    # sync_table(ProductList)
    # mc = ProductList(pname='a', dname='A', required_items=['a', 'b'], category='mic', pid=uuid.uuid1())
    # mc.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('hello')
        test_cassandra()
