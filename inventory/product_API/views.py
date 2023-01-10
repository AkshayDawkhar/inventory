from rest_framework.views import APIView
from rest_framework.response import Response
from .cqlqueries import ProductCQL, DatabaseError

p = ProductCQL()


class ProductList(APIView):
    def get(self, request):
        a = p.product_list()
        return Response(a)


class GetProduct(APIView):
    def get(self, request, pid):
        try:
            a = p.get_product(pid=pid)
        except DatabaseError:
            return Response(data={'error': 'Product Not Found %s' % (pid,)},
                            status=404)
        print(a)
        return Response(a)
