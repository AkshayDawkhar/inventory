# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import BuildCQL, NotFound

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
