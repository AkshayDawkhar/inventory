from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid
from productapi.models import ProductList
from productapi.serializers import Plistserializer
from cassandra.cqlengine import columns, connection
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from productapi.cqlqueries import ProductCQL,DatabaseError
# from rest_framework.serializers import Serializer
# Create your views here.
cluster = Cluster(['127.0.0.1'])
sec = cluster.connect()
con = connection.register_connection('cluster',session=sec)
secs = cluster.connect('model1')
sec.row_factory = dict_factory
p=ProductCQL()
@api_view(['GET','POST'])
def product_list(request):
    a=p.prduct_list()
    return Response(a)    
@api_view(['GET','POST'])
def get_product(request,pid):
    try :
        a=p.get_product(pid=pid)
    except DatabaseError :
        return Response({'error':'Product Not Found %s' %(pid,)},status=404)
    print(a)
    return Response(a)