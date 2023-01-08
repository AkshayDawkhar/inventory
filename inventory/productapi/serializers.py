from rest_framework import serializers
# from rest_framework.fields import UUIDField
import re
class low(serializers.CharField):
    def to_internal_value(self, data):
        return re.sub(r'[^\w\s]', '', data.lower())
color_choices=['','red','blue','black']
required_iteam_choices=['row1','row2','row3']
class Plistserializer(serializers.Serializer):
    pname=low()
    color=serializers.ChoiceField(color_choices,default='black')
    required_iteams = serializers.ListField(child=serializers.ChoiceField(required_iteam_choices))
    category=low()
    pid=serializers.UUIDField()
    # def validate(self, data):
    #     if data['fname'] not in a:
    #         raise serializers.ValidationError("fname is 0")
    #     return data