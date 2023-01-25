from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import ProductCQL, DatabaseError, NotFound, Conflict
from .serializers import CreateProductSerializer, UpdateProductSerializer, InvalidDname
from rest_framework import status
from build_API.cqlqueries import BuildCQL

p = ProductCQL()
b = BuildCQL()


class ProductList(APIView):
    def get(self, request):
        # get all product
        return Response(data=p.product_list(), status=status.HTTP_200_OK)

    def post(self, request):
        # code for creating product
        sp = CreateProductSerializer(data=request.data)
        try:
            if sp.is_valid():
                pid = p.get_pid(sp.data.get('pname'), sp.data.get('color'),sp.data.get('required_items'))
                b.create_build(pid=pid)
                return Response(data=p.product_list())
            # print(sp.errors)
        except InvalidDname:
            return Response(data={"dname": ["Invalid Name"]}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(sp.errors,
                        status=status.HTTP_226_IM_USED if 'error' in sp.errors else status.HTTP_400_BAD_REQUEST)


class Product(APIView):
    def get(self, request, pid):
        try:
            a = p.get_product(pid=pid)
        except DatabaseError:
            return Response(data={'error': 'Product Not Found %s' % (pid,)},
                            status=status.HTTP_404_NOT_FOUND)
        # print(a)
        return Response(a)

    def put(self, request, pid):
        # data = request.data
        sp = UpdateProductSerializer(data=request.data)
        try:
            if sp.is_valid():
                a = p.update_product(pid=pid, pname=sp.data.get('pname'), color=sp.data.get('color'),
                                     required_items=sp.data.get('required_items'), dname=sp.data.get('dname'),
                                     category=sp.data.get('category'),
                                     required_items_no=sp.data.get('required_items_no'))
            else:
                return Response(data=sp.errors, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response(data={'error': 'Product Not Found %s' % (pid,)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidDname:
            return Response(data={"dname": ["Invalid Name"]}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Conflict:
            return Response(
                data={"error": "Same Product Exists %s\n%s\n%s" % (
                    sp.data.get('pname'), sp.data.get('color'), sp.data.get('required_items'))},
                status=status.HTTP_409_CONFLICT)
        return self.get(request, pid)

    def delete(self, request, pid):
        try:
            p.delete_product(pid=pid)
        except NotFound:
            return Response(data={'error': 'Product Not Found %s' % (pid,)},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(data=p.product_list(), status=status.HTTP_202_ACCEPTED)


class Trashes(APIView):
    def get(self, request):
        return Response(p.get_trashes(), status=status.HTTP_200_OK)


class Trash(APIView):
    def get(self, request, pid):
        try:
            a = p.get_trash(pid)
            return Response(a, status=status.HTTP_200_OK)
        except NotFound:
            return Response(data={'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pid):
        try:
            p.restore(pid)
            return Response(data=p.get_trashes(), status=status.HTTP_200_OK)
        except Conflict:
            return Response(data={'error': 'same product Already Exists '}, status=status.HTTP_409_CONFLICT)
        except DatabaseError:
            return Response(data={'error': 'Product does not exists in Trash'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pid):
        p.delete_trash(pid)
        return Response(data=p.get_trashes(), status=status.HTTP_200_OK)
