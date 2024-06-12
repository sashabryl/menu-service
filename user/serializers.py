from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError as RESTValidationError
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "password", "confirm_password")

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise RESTValidationError("Passwords don't match")
        del data["confirm_password"]
        return super().validate(data)

    @staticmethod
    def validate_password(value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise RESTValidationError(str(exc))
        return value

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
