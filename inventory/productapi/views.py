from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid
from productapi.models import ProductList
from productapi.serializers import Plistserializer
from cassandra.cqlengine import columns, connection
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
# from rest_framework.serializers import Serializer
# Create your views here.
cluster = Cluster(['127.0.0.1'])
sec = cluster.connect()
con = connection.register_connection('cluster',session=sec)
secs = cluster.connect('model1')
sec.row_factory = dict_factory
@api_view(['GET','POST'])
def productlist(request):
    d={'pname': 'a', 'color': 'black', 'category': 'mic', 'pid':uuid.uuid4(), 'required_iteams': ['a', 'b']}
    if request.method == 'POST':
        d=request.data
        d['pid']=uuid.uuid4()
    pls= Plistserializer(data=d)
    if pls.is_valid():
        print('------------------------------------------valid',sep='\n')
        p=ProductList(**pls.data)
        p.save()
        #a=ProductList.all()
        rs= sec.execute("SELECT * FROM model1.product_list")

        for r in rs:
            print(dict(r))
            rpls= Plistserializer(data=dict(r))
            if rpls.is_valid():
                print('================================-===========================valid')
        return Response(rpls.data,status=201)
    else:
        print('---------------------------------------not valid',sep='\n')
    return Response({})