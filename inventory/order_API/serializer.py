from rest_framework import serializers


class EditOrderSerializers(serializers.Serializer):
    timestamp = serializers.FloatField()
    numbers = serializers.IntegerField()


class GetOrderSerializers(serializers.Serializer):
    timestamp = serializers.FloatField()
