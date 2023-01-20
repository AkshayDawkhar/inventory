# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response


class BuildProducts(APIView):
    def get(self, request):
        return Response(data={}, status=200)
