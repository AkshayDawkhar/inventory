from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid
from productapi.serializers import Plistserializer
# from rest_framework.serializers import Serializer
# Create your views here.

@api_view(['GET','POST'])
def productlist(request):
    d={'fname':10,'mname':'a','lname':'1','rname':[['1']]}
    pls= Plistserializer(data=d)
    if pls.is_valid():
        print('------------------------------------------valid',uuid.uuid4(),uuid.uuid1(),sep='\n')
        return Response(pls.data,status=201)
    else:
        print('---------------------------------------not valid',pls.data.get('fname'),sep='\n')
    return Response({})