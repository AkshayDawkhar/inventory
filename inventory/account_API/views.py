from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import cqlqueries as accoutCQL
from .serializers import CreateWorkerSerializer


# Create your views here.
class accounts(APIView):
    def get(self, request):
        workers = accoutCQL.get_workers()
        return Response(data=workers, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateWorkerSerializer(data=request.data)
        if serializer.is_valid():
            worker = accoutCQL.create_worker(**serializer.data)
            if worker:
                return Response(data='error':['user Already Exists'],status=status.HTTP_208_ALREADY_REPORTED)
        return Response(data=accoutCQL.get_workers(), status=status.HTTP_200_OK)
