from rest_framework.decorators import api_view
from rest_framework.response import Response

from .cqlqueries import ProductCQL, DatabaseError

p = ProductCQL()


# class

@api_view(['GET', 'POST'])
def product_list(request):
    a = p.product_list()
    return Response(a)


@api_view(['GET', 'POST'])
def get_product(request, pid):
    try:
        a = p.get_product(pid=pid)
    except DatabaseError:
        return Response(data={'error': 'Product Not Found %s' % (pid,)},
                        status=404)
    print(a)
    return Response(a)
