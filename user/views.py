from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from user.serializers import UserCreateSerializer


class CreateEmployee(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        return serializer.save(is_employee=True)
