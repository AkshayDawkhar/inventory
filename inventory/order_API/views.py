from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import cqlqueries as order_cql
from .serializer import EditOrderSerializers


# Create your views here.

class Orders(APIView):
    def get(self, request):
        orders = order_cql.get_orders()
        return Response(data=orders, status=status.HTTP_200_OK)


class Order(APIView):
    def post(self, request, pid):
        serializers = EditOrderSerializers(data=request.data)
        if serializers.is_valid():
            order_cql.add_order(pid=pid, date=serializers.data.get('timestamp'),
                                numbers=serializers.data.get('numbers'))
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pid):
        serializers = EditOrderSerializers(data=request.data)
        if serializers.is_valid():
            order_cql.edit_orders(pid=pid, ts=serializers.data.get('timestamp'),
                                  numbers=serializers.data.get('numbers'))
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
