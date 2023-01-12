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
        attrs['pname'] = re.sub('[^A-Za-z0-9]+', '', attrs['dname'].lower())
        return attrs


class CreateProductSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    pname = low(required=False)
    dname = serializers.CharField()
    color = serializers.ChoiceField(color_choices, default='black')
    required_items = serializers.ListField(child=serializers.ChoiceField(required_item_choices))
    category = serializers.CharField()
    def validate(self, attrs):
        attrs['pname'] = re.sub('[^A-Za-z0-9]+', '', attrs['dname'].lower())
        # if attrs['pname'] == 'red':
            # raise serializers.ValidationError('nothing valid')
        return attrs
    def validated_dname(self,val):
        if val['pname'] == 'red':
            print('---------------------------')
            raise serializers.ValidationError('nothing valid really')
        raise serializers.ValidationError('nothing valid12')
        return val