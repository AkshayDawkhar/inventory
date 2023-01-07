from django.core.management.base import BaseCommand
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns, connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table,create_keyspace_simple
from productapi.models import ProductList
import os,uuid
def testCassandra():
    #for a -->  UserWarning: CQLENG_ALLOW_SCHEMA_MANAGEMENT environment variable is not set. Future versions of this package will require this variable to enable management functions.
    if os.getenv('CQLENG_ALLOW_SCHEMA_MANAGEMENT') is None:
        os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'
    
    cluster = Cluster(['127.0.0.1'])
    sec = cluster.connect()
    print('connected to the db')
    con = connection.register_connection('cluster',session=sec)
    create_keyspace_simple('model1', 1,connections=['cluster'])
    print('synchronizing db ')
    sync_table(ProductList)
    mc=ProductList(pname='a',required_iteams=['a','b'],category='mic',pid=uuid.uuid1())
    mc.save()

class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        print('hello')
        testCassandra()