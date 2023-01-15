from rest_framework import serializers
# from rest_framework.fields import UUIDField
import re
from .cqlqueries import ProductCQL, DatabaseError


class Already_Exist(Exception):
    pass


p = ProductCQL()


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
        attrs['pname'] = re.sub('[^A-Za-z0-9]+', '', attrs['dname'].lower())
        return attrs


class CreateProductSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    error_massages = {
        'pname': 'ok',
        'dname': 'ok',
        'color': 'ok',
        'required_items': [],
        'category': 'ok',
    }
    pname = low(required=False)
    dname = serializers.CharField()
    color = serializers.ChoiceField(color_choices, default='black')
    required_items = serializers.ListField(child=serializers.ChoiceField(required_item_choices))
    category = serializers.CharField()

    def validate(self, attrs):
        attrs['pname'] = re.sub('[^A-Za-z0-9]+', '', attrs['dname'].lower())
        try:
            pid = p.get_pid(pname=attrs['pname'], color=attrs['color'], required_items=attrs['required_items'])
            raise serializers.ValidationError({'error': 'Already Exist'})
        except DatabaseError:
            p.create_product(pname=attrs['pname'], required_items =attrs['required_items'],
                             color=attrs['color'], category=attrs['category'], dname=attrs['dname'])
            # raise serializers.ValidationError(self.error_massages, code='valid')
        return attrs
