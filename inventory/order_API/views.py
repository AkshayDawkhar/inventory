from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import cqlqueries as order_cql
from .serializer import EditOrderSerializers, GetOrderSerializers


# Create your views here.

class Orders(APIView):
    def get(self, request):
        orders = order_cql.get_orders()
        return Response(data=orders, status=status.HTTP_200_OK)


class EditOrder(APIView):

    def get(self, request, pid):
        serializers = GetOrderSerializers(data=request.data)
        if serializers.is_valid():
            order = order_cql.get_order(serializers.data.get('timestamp'), pid)
            return Response(data=order, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pid):
        serializers = EditOrderSerializers(data=request.data)
        if serializers.is_valid():
            order_cql.add_order(pid=pid, date=serializers.data.get('timestamp'),
                                numbers=serializers.data.get('numbers'))
            order = order_cql.get_order(serializers.data.get('timestamp'), pid)
            if order is None:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
            return Response(data=order, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pid):
        serializers = EditOrderSerializers(data=request.data)
        if serializers.is_valid():
            order_cql.remove_order(pid=pid, date=serializers.data.get('timestamp'),
                                numbers=serializers.data.get('numbers'))
            order = order_cql.get_order(serializers.data.get('timestamp'), pid)
            if order is None:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
            return Response(data=order, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pid):
        serializers = EditOrderSerializers(data=request.data)
        if serializers.is_valid():
            order_cql.edit_orders(pid=pid, ts=serializers.data.get('timestamp'),
                                  numbers=serializers.data.get('numbers'))
            order = order_cql.get_order(serializers.data.get('timestamp'), pid)
            if order is None:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
            return Response(order, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
