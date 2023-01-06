from django.core.management.base import BaseCommand
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
cluster = Cluster(['127.0.0.1'])
sec = cluster.connect()
con = connection.register_connection('cluster2',session=sec)
class mccdr(Model):
    __connection__= 'cluster2'
    __table_name__='mccdr'
    __keyspace__='model1'
    fname=columns.Integer(primary_key=True)
    mname=columns.Text()
    lname=columns.Text()
    Meta = {
        'cluster': cluster
    }

class Command(BaseCommand):
    # def handle_noargs(self, **options):
        # cluster = Cluster(['127.0.0.1'])
    def handle(self,*args,**kwargs):
        print('hello')
        mc=mccdr(fname=12,mname='a',lname='b')
        mc.save()




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