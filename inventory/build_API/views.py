# Create your views here.
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import BuildCQL, NotFound
from .serializer import RequiredItemSerializer
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
            b.create_required_items(pid=uuid.UUID(s.data.get('pid')), rid=uuid.UUID(s.data.get('rid')),
                                    numbers=s.data.get('numbers'))
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
