# Create your views here.
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import BuildCQL, NotFound, InvalidNumber
from .serializer import RequiredItemSerializer, BuildProductSerializer, DiscardProductSerializer, StockProductSerializer
from rest_framework import status

b = BuildCQL()


class BuildProducts(APIView):
    def get(self, request):
        return Response(data=b.get_builds(), status=status.HTTP_200_OK)


class EditBuildProduct(APIView):
    # to get product using uuid
    def get(self, request, pid):
        try:
            r = b.get_build(pid)
        except NotFound:
            return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=r, status=status.HTTP_200_OK)

    def put(self, request, pid):
        serializer = BuildProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                b.edit_building(pid, serializer.data.get('build_no'))
                build = b.get_build(pid)
                return Response(data=build, status=status.HTTP_200_OK)
            except NotFound:
                return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)


class BuildProduct(APIView):
    def get(self, request, pid):
        a = b.get_max_builds(pid)
        return Response(a, status=status.HTTP_200_OK)

    def post(self, request, pid):
        serializer = BuildProductSerializer(data=request.data)
        if serializer.is_valid():
            numbers = serializer.data.get('build_no')
            try:
                build = b.safe_build(pid, numbers)
                if build < 0:
                    return Response(data={'error': 'max build value is %d' % (numbers + build)},
                                    status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
                return Response(data=b.get_build(pid), status=status.HTTP_200_OK)
            except NotFound:
                return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pid):
        serializer = DiscardProductSerializer(data=request.data)
        if serializer.is_valid():
            numbers = serializer.data.get('discard_no')
            build = b.safe_discard(pid, numbers)
            if build < 0:
                return Response(data={'error': 'max build value is %d' % (numbers + build)},
                                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
            return Response(data=b.get_build(pid), status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class EditStock(APIView):
    def put(self, request, pid):
        serializer = StockProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                b.edit_stock(pid, serializer.data.get('stock_no'))
                build = b.get_build(pid=pid)
                return Response(data=build, status=status.HTTP_200_OK)
            except NotFound:
                return Response(data={'error': 'product Not Found'}, status=status.HTTP_404_NOT_FOUND)


class Stock(APIView):
    def post(self, request, pid):
        ss = StockProductSerializer(data=request.data)
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
        ss = StockProductSerializer(data=request.data)
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


class GetNeeded(APIView):
    def get(self, request, pid):
        needed = b.generate_needed(pid)
        return Response(data=needed,status=status.HTTP_200_OK)