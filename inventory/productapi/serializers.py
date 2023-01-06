from rest_framework import serializers
# from rest_framework.fields import UUIDField
class low(serializers.CharField):
    def to_internal_value(self, data):
        return data.lower()
a=[1,2,3,4,5,6]
class Plistserializer(serializers.Serializer):
    fname=serializers.IntegerField()
    mname=serializers.CharField()
    lname=low()
    rname=serializers.ListField(child=serializers.ListField(child=serializers.IntegerField()))
    # rname=ListField(child=serializers.IntegerField())
    def validate(self, data):
        if data['fname'] not in a:
            raise serializers.ValidationError("fname is 0")
        return data