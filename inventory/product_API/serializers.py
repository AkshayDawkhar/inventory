from rest_framework import serializers
# from rest_framework.fields import UUIDField
import re


class low(serializers.CharField):
    def to_internal_value(self, data):
        return re.sub(r'[^\w\s]', '', data.lower())


color_choices = ['', 'red', 'blue', 'black']
required_item_choices = ['row1', 'row2', 'row3']


class ProductListSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    dname = serializers.CharField()
    pname = low(required=False)
    color = serializers.ChoiceField(color_choices, default='black')
    required_items = serializers.ListField(child=serializers.ChoiceField(required_item_choices))
    category = low()
    pid = serializers.UUIDField()

    def validate(self, attrs):
        attrs['pname'] = re.sub(r'[^\w\s]', '', attrs['dname'].lower())
        return attrs
