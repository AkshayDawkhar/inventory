from rest_framework import serializers


class RequiredItemSerializer(serializers.Serializer):
    pid = serializers.UUIDField()
    rid = serializers.UUIDField()
    numbers = serializers.IntegerField(min_value=1)
