from django.core.management.base import BaseCommand
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table,create_keyspace_simple
import os
class mccdr(Model):
    __connection__= 'cluster'
    __table_name__='mccdr'
    __keyspace__='model1'
    fname=columns.Integer(primary_key=True)
    mname=columns.Text()
    lname=columns.Text()
    # Meta = {
    #     'cluster': cluster
    # }
def testCassandra():
    #for a error  UserWarning: CQLENG_ALLOW_SCHEMA_MANAGEMENT environment variable is not set. Future versions of this package will require this variable to enable management functions.
    if os.getenv('CQLENG_ALLOW_SCHEMA_MANAGEMENT') is None:
        os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'
    
    cluster = Cluster(['127.0.0.1'])
    sec = cluster.connect()
    con = connection.register_connection('cluster',session=sec)
    create_keyspace_simple('model1', 1,connections=['cluster'])
    sync_table(mccdr)
    mc=mccdr(fname=11,mname='a',lname='b')
    mc.save()

class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        print('hello')
        testCassandra()
        



        # aka=ak(13)
        # aka.geta()
        # ak.geta(aka)

# class ak:
#     i=0
#     def __init__(self,ii):
#         self.i=ii
#         print('---------------12---------12-----------12-----12')
#     def geta(self):
#         print(12,self.i)