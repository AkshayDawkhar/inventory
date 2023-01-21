# Create your views here.
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import BuildCQL, NotFound
from .serializer import RequiredItemSerializer

b = BuildCQL()


class BuildProducts(APIView):
    def get(self, request):
        return Response(data=b.get_builds(), status=200)


class BuildProduct(APIView):
    def get(self, request, pid):
        try:
            r = b.get_build(pid)
        except NotFound:
            return Response(data={'error': 'product Not Found'}, status=404)
        return Response(data=r, status=200)


class RequiredItem(APIView):
    def get(self, request, pid):
        a = b.get_required_items(pid)
        return Response(data=a, status=200)

    def delete(self, request, pid):
        a = b.delete_required_items(pid)
        return Response(data=a, status=200)


class RequiredItems(APIView):
    def post(self, request):
        s = RequiredItemSerializer(data=request.data)
        if s.is_valid():
            b.create_required_items(pid=uuid.UUID(s.data.get('pid')), rid=uuid.UUID(s.data.get('rid')),
                                    numbers=s.data.get('numbers'))
            return Response(data={}, status=200)
        else:
            return Response(data=s.errors, status=406)
