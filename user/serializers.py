from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    fields = ("username", "password")
