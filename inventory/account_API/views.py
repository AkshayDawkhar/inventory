from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import cqlqueries as accoutCQL
from .serializers import CreateWorkerSerializer, CreateAdminSerializer, UpdateSerializer, UpdatePasswordSerializer
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
class accounts(APIView):
    def get(self, request):
        workers = accoutCQL.get_workers()
        return Response(data=workers, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateWorkerSerializer(data=request.data)
        if serializer.is_valid():
            worker = accoutCQL.create_worker(f_name=serializer.data.get('f_name'), l_name=serializer.data.get('l_name'),
                                             username=serializer.data.get('username'),
                                             password=make_password(serializer.data.get('password')))
            if not worker:
                return Response(data={'error': ['user Already Exists']}, status=status.HTTP_208_ALREADY_REPORTED)
            return Response(data=accoutCQL.get_workers(), status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class account(APIView):
    def get(self, request, username):
        worker = accoutCQL.get_workers(username=username)
        if worker is None:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        return Response(data=worker, status=status.HTTP_200_OK)

    def put(self, request, username):
        serializer = UpdateSerializer(data=request.data)
        if serializer.is_valid():
            applied = accoutCQL.update_worker(username=username, f_name=serializer.data.get('f_name'),
                                              l_name=serializer.data.get('l_name'))
            if not applied:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)
            return Response(data=accoutCQL.get_workers(username=username), status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get('previous_password') != serializer.data.get('password'):
                if check_password(serializer.data.get('previous_password'), accoutCQL.get_worker_password(username=username)):
                    if not accoutCQL.update_worker_password(username=username,
                                                            password=make_password(serializer.data.get('password'))):
                        return Response(data=None, status=status.HTTP_404_NOT_FOUND)
                    return Response(data=accoutCQL.get_workers(username=username), status=status.HTTP_200_OK)
                else:
                    return Response(data={'error': ['invalid previous password']},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response(data={'error': ['previous password and password is same']}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class admins(APIView):
    def get(self, request):
        admins = accoutCQL.get_admins()
        return Response(data=admins, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateAdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = accoutCQL.create_admin(f_name=serializer.data.get('f_name'), l_name=serializer.data.get('l_name'),
                                           username=serializer.data.get('username'),
                                           password=make_password(serializer.data.get('password')))
            if not admin:
                return Response(data={'error': ['user Already Exists']}, status=status.HTTP_208_ALREADY_REPORTED)
            return Response(data=accoutCQL.get_admins(), status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class admin(APIView):
    def get(self, request, username):
        admins = accoutCQL.get_admins(username=username)
        return Response(data=admins, status=status.HTTP_200_OK)

    def put(self, request, username):
        serializer = UpdateSerializer(data=request.data)
        if serializer.is_valid():
            applied = accoutCQL.update_admin(username=username, f_name=serializer.data.get('f_name'),
                                             l_name=serializer.data.get('l_name'))
            if not applied:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)
            return Response(data=accoutCQL.get_admins(username=username), status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not accoutCQL.update_admin_password(username=username,
                                                   password=make_password(serializer.data.get('password'))):
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)
            return Response(data=accoutCQL.get_admins(username=username), status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
