from rest_framework import serializers


class CreateWorkerSerializer(serializers.Serializer):
    f_name = serializers.CharField()
    l_name = serializers.CharField()
    password = serializers.CharField()
