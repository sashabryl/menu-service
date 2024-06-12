import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response

from menu.models import Menu, Vote
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
        .order_by("-num_votes")
    )
    permission_classes = [IsEmployee]


@api_view(["POST"])
def vote_for_menu(request, pk: int):

    if not request.user.is_authenticated:
        raise NotAuthenticated()
    if not request.user.is_employee:
        raise PermissionDenied()

    menu = get_object_or_404(Menu, id=pk)
    if Vote.objects.filter(user=request.user, created_at=datetime.date.today()):
        return Response("You have already voted today.")

    with transaction.atomic():
        Vote.objects.create(menu=menu, user=request.user)
        menu.num_votes += 1
        menu.save()

    return Response("Thank you for your civic awareness!")
