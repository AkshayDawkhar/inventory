from rest_framework import serializers


class CreateWorkerSerializer(serializers.Serializer):
    username = serializers.CharField(default=None)
    f_name = serializers.CharField()
    l_name = serializers.CharField()
    password = serializers.CharField()
