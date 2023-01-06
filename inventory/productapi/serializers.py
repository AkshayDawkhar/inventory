from rest_framework import serializers
# from rest_framework.fields import UUIDField
class low(serializers.CharField):
    def to_internal_value(self, data):
        return data.lower()

class Plistserializer(serializers.Serializer):
    fname=serializers.IntegerField()
    mname=serializers.CharField()
    lname=low()
    rname=serializers.ListField(child=serializers.ListField(child=serializers.IntegerField()))
    # rname=ListField(child=serializers.IntegerField())