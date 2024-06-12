import datetime

from rest_framework.generics import CreateAPIView, ListAPIView

from menu.models import Menu
from menu.permissions import IsRestaurant, IsEmployee
from menu.serializers import MenuUploadSerializer, MenuListSerializer


class UploadMenu(CreateAPIView):
    serializer_class = MenuUploadSerializer
    queryset = (
        Menu.objects
        .select_related("restaurant")
        .prefetch_related("votes")
        .all()
    )
    permission_classes = [IsRestaurant]

    def perform_create(self, serializer):
        return serializer.save(restaurant=self.request.user)


class ListMenu(ListAPIView):
    serializer_class = MenuListSerializer
    queryset = (
        Menu.objects
        .select_related("restaurant")
        .prefetch_related("votes")
        .filter(created_at=datetime.date.today())
        .all()
        .order_by("-num_votes")
    )
    permission_classes = [IsEmployee]

