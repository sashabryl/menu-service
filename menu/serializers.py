from rest_framework import serializers

from menu.models import Menu


class MenuUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("name", "description")


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("name", "description", "num_votes", "created_at")
