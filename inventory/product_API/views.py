from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import ProductCQL, DatabaseError, NotFound, Conflict
from .serializers import CreateProductSerializer, UpdateProductSerializer, InvalidDname

p = ProductCQL()


class ProductList(APIView):
    def get(self, request):
        # get all product
        return Response(data=p.product_list(), status=200)

    def post(self, request):
        # code for creating product
        sp = CreateProductSerializer(data=request.data)
        if sp.is_valid():
            return Response(data=p.product_list())
        # print(sp.errors)

        return Response(sp.errors, status=226 if 'error' in sp.errors else 400)


class Product(APIView):
    def get(self, request, pid):
        try:
            a = p.get_product(pid=pid)
        except DatabaseError:
            return Response(data={'error': 'Product Not Found %s' % (pid,)},
                            status=404)
        # print(a)
        return Response(a)

    def put(self, request, pid):
        # data = request.data
        sp = UpdateProductSerializer(data=request.data)
        try:
            if sp.is_valid():
                a = p.update_product(pid=pid, pname=sp.data.get('pname'), color=sp.data.get('color'),
                                     required_items=sp.data.get('required_items'), dname=sp.data.get('dname'),
                                     category=sp.data.get('category'))
            else:
                return Response(data=sp.errors, status=400)
        except NotFound:
            return Response(data={'error': 'Product Not Found %s' % (pid,)}, status=404)
        except InvalidDname:
            return Response(data={"dname": ["Invalid Name"]}, status=406)
        except Conflict:
            return Response(
                data={"error": "Same Product Exists %s\n%s\n%s" % (sp.data.get('pname'), sp.data.get('color'), sp.data.get('required_items'))},
                status=409)
        return self.get(request, pid)

    def delete(self, request, pid):
        try:
            p.delete_product(moveto_trash=False, pid=pid)
        except NotFound:
            return Response(data={'error': 'Product Not Found %s' % (pid,)},
                            status=404)
        return Response(data=p.product_list(), status=202)
