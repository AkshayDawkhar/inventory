from rest_framework import serializers


class CreateWorkerSerializer(serializers.Serializer):
    username = serializers.CharField(default=None)
    f_name = serializers.CharField()
    l_name = serializers.CharField()
    password = serializers.CharField()


class CreateAdminSerializer(serializers.Serializer):
    username = serializers.CharField(default=None)
    f_name = serializers.CharField()
    l_name = serializers.CharField()
    password = serializers.CharField()


class UpdateSerializer(serializers.Serializer):
    f_name = serializers.CharField()
    l_name = serializers.CharField()


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()