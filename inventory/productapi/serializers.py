from rest_framework import serializers
# from rest_framework.fields import UUIDField
class low(serializers.CharField):
    def to_internal_value(self, data):
        return data.lower()
        
class Plistserializer(serializers.Serializer):
    pname=serializers.CharField()
    color=serializers.CharField()
    required_iteams = serializers.ListField(child=serializers.CharField())
    category=serializers.CharField()
    pid=serializers.UUIDField()
    # def validate(self, data):
    #     if data['fname'] not in a:
    #         raise serializers.ValidationError("fname is 0")
    #     return data