# Create your views here.
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import BuildCQL, NotFound, InvalidNumber
from .serializer import RequiredItemSerializer, BuildProductSerializer, DiscardProductSerializer, StockProductSerialzer
from rest_framework import status

b = BuildCQL()


class BuildProducts(APIView):
    def get(self, request):
        return Response(data=b.get_builds(), status=status.HTTP_200_OK)


class BuildProduct(APIView):
    def get(self, request, pid):
        try:
            r = b.get_build(pid)
        except NotFound:
            return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=r, status=status.HTTP_200_OK)

    def post(self, request, pid):
        bs = BuildProductSerializer(data=request.data)
        if bs.is_valid():
            b.build_product(pid, numbers=bs.data.get('build_no'))
            return self.get(request, pid)
        else:
            return Response(data=bs.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pid):
        ds = DiscardProductSerializer(data=request.data)
        if ds.is_valid():
            try:
                b.discard_product(pid, numbers=ds.data.get('discard_no'))
                return self.get(request, pid)
            except InvalidNumber:
                return Response(data={'discard_no': ["Ensure this value is less than or equal to level ."]},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except NotFound:
                return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=ds.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pid):
        try:
            a = b.delete_build(pid)
            if a:
                return Response(data={}, status=201)
        except NotFound:
            return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)


class RequiredItem(APIView):
    def get(self, request, pid):
        a = b.get_required_items(pid)
        return Response(data=a, status=status.HTTP_200_OK)

    def delete(self, request, pid):
        a = b.delete_required_items(pid)
        return Response(data=a, status=status.HTTP_200_OK)


class RequiredItems(APIView):
    def post(self, request):
        s = RequiredItemSerializer(data=request.data)
        if s.is_valid():
            b.create_required_item(pid=uuid.UUID(s.data.get('pid')), rid=uuid.UUID(s.data.get('rid')),
                                   numbers=s.data.get('numbers'))
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class RequiredFor(APIView):
    def get(self, request, rid):
        a = b.get_req_items_by_rid(rid=rid)
        return Response(data=a, status=status.HTTP_200_OK)


class Stock(APIView):
    def post(self, request, pid):
        ss = StockProductSerialzer(data=request.data)
        if ss.is_valid():
            try:
                b.add_stock(pid=pid, numbers=ss.data.get('stock_no'))
                a = b.get_build(pid=pid)
                return Response(data=a, status=status.HTTP_226_IM_USED)
            except InvalidNumber:
                return Response(data={'stock_no': ["Ensure this value is less than or equal to level ."]},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except NotFound:
                return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=ss.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pid):
        ss = StockProductSerialzer(data=request.data)
        if ss.is_valid():
            try:
                b.discard_stock(pid=pid, numbers=ss.data.get('stock_no'))
                a = b.get_build(pid)
                return Response(data=a, status=status.HTTP_200_OK)
            except InvalidNumber:
                return Response(data={'stock_no': ["Ensure this value is less than or equal to level ."]},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except NotFound:
                return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(data=ss.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMax(APIView):
    def get(self, request, pid):
        a = b.get_max_builds(pid)
        return Response(a, status=status.HTTP_200_OK)
