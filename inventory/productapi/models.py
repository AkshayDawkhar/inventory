# from django.db import models
from cassandra.cqlengine.models import Model,columns
# Create your models here.
class mccdr(Model):
    __connection__= 'cluster'
    __table_name__='mccdr'
    __keyspace__='model1'
    fname=columns.Integer(primary_key=True)
    # mname=columns.Text()
    lname=columns.Text()
    oname=columns.Text()