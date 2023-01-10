from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import ProductCQL, DatabaseError
from django.shortcuts import redirect

p = ProductCQL()


class ProductList(APIView):
    def get(self, request):
        # get all products
        return Response(data=p.product_list(), status=200)

    def post(self, request):
        # code for creating product
        return Response(data=p.product_list(), status=201)


class Product(APIView):
    def get(self, request, pid):
        try:
            a = p.get_product(pid=pid)
        except DatabaseError:
            return Response(data={'error': 'Product Not Found %s' % (pid,)},
                            status=404)
        print(a)
        return Response(a)

    def put(self, request, pid):
        # code for editing the product
        return Response(data={}, status=200)
