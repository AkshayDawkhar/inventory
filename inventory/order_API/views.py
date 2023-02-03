from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import cqlqueries as order_cql

# Create your views here.

class Orders(APIView):
    def get(self, request):
        orders = order_cql.get_orders()
        return Response(data=orders, status=status.HTTP_200_OK)
