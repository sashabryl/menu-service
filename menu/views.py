from rest_framework.generics import CreateAPIView, ListAPIView

from menu.models import Menu
from menu.permissions import IsRestaurant
from menu.serializers import MenuUploadSerializer


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
