from rest_framework import serializers


class CreateWorkerSerializer(serializers.Serializer):
    username = serializers.CharField()
    f_name = serializers.CharField()
    l_name = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=32)
    mail = serializers.EmailField()


class CreateAdminSerializer(serializers.Serializer):
    username = serializers.CharField()
    f_name = serializers.CharField()
    l_name = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=32)
    mail = serializers.EmailField()


class UpdateSerializer(serializers.Serializer):
    f_name = serializers.CharField()
    l_name = serializers.CharField()


class UpdatePasswordSerializer(serializers.Serializer):
    previous_password = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=32)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class GenerateUsernameSerializer(serializers.Serializer):
    f_name = serializers.CharField()
    l_name = serializers.CharField()