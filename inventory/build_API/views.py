# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import BuildCQL

b = BuildCQL()


class BuildProducts(APIView):
    def get(self, request):
        return Response(data=b.get_builds(), status=200)


class BuildProduct(APIView):
    def get(self, request, pid):
        return Response(data=b.get_build(pid), status=200)
