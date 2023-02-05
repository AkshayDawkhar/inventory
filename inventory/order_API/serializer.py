from rest_framework import serializers


class EditOrderSerializers(serializers.Serializer):
    timestamp = serializers.FloatField()
    numbers = serializers.IntegerField()
