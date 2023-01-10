import os
import uuid

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from django.core.management.base import BaseCommand
from product_API.models import ProductList


def test_cassandra():
    # for a -->  UserWarning: CQLENG_ALLOW_SCHEMA_MANAGEMENT environment variable is not set. Future versions of this
    # package will require this variable to enable management functions.
    if os.getenv('CQLENG_ALLOW_SCHEMA_MANAGEMENT') is None:
        os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

    cluster = Cluster(['127.0.0.1'])
    sec = cluster.connect()
    print('connected to the db')
    con = connection.register_connection('cluster', session=sec)
    create_keyspace_simple('model1', 1, connections=['cluster'])
    print('synchronizing db ')
    sync_table(ProductList)
    mc = ProductList(pname='a', dname='A', required_items=['a', 'b'], category='mic', pid=uuid.uuid1())
    mc.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('hello')
        test_cassandra()
