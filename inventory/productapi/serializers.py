from rest_framework import serializers
# from rest_framework.fields import UUIDField
import re
class low(serializers.CharField):
    def to_internal_value(self, data):
        return re.sub(r'[^\w\s]', '', data.lower())

color_choices=['','red','blue','black']
required_iteam_choices=['row1','row2','row3']
class Plistserializer(serializers.Serializer):
    dname=serializers.CharField()
    pname=low(required=False)
    color=serializers.ChoiceField(color_choices,default='black')
    required_iteams = serializers.ListField(child=serializers.ChoiceField(required_iteam_choices))
    category=low()
    pid=serializers.UUIDField()
    
    def validate(self, attrs):
        attrs['pname'] = re.sub(r'[^\w\s]', '',attrs['dname'].lower())
        return attrs