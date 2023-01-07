from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid
from productapi.serializers import Plistserializer
# from rest_framework.serializers import Serializer
# Create your views here.

@api_view(['GET','POST'])
def productlist(request):
    d={"pname": "a", "color": "black", "category": "mic", "pid": "d4ed279c-8e83-11ed-a144-f889d2e645af", "required_iteams": ["a", "b"]}
    pls= Plistserializer(data=d)
    if pls.is_valid():
        print('------------------------------------------valid',sep='\n')
        return Response(pls.data,status=201)
    else:
        print('---------------------------------------not valid',pls.data.get('fname'),sep='\n')
    return Response({})