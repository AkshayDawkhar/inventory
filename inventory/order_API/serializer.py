from rest_framework import serializers


class EditOrderSerializers(serializers.Serializer):
    date = serializers.DateField()
    numbers = serializers.IntegerField()