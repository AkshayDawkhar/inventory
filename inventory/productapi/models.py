# from django.db import models
from cassandra.cqlengine.models import Model,columns
# Create your models here.
class ProductList(Model):
    __connection__= 'cluster'
    __table_name__='product_list'
    __keyspace__='model1'
    pname=columns.Text(primary_key=True)
    dname=columns.Text()
    color=columns.Text(primary_key=True,default='black')
    required_iteams =columns.Set(columns.Text())
    category = columns.Text()
    pid=columns.UUID()