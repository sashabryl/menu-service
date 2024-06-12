import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.exceptions import (
    NotAuthenticated,
    ValidationError,
    PermissionDenied,
)
from rest_framework.response import Response

from menu.models import Menu, Vote
from menu.permissions import IsRestaurant, IsEmployee
from menu.serializers import (
    MenuUploadSerializer,
    MenuListSerializer,
    MenuListSerializerEmployee,
)


class UploadMenu(CreateAPIView):
    """
    One restaurant can upload only one menu a day.
    """

    serializer_class = MenuUploadSerializer
    queryset = (
        Menu.objects.select_related("restaurant")
        .prefetch_related("votes")
        .all()
    )
    permission_classes = [IsRestaurant]

    def perform_create(self, serializer):
        if self.queryset.filter(
            restaurant=self.request.user, created_at=datetime.date.today()
        ):
            raise ValidationError(
                detail="You have already uploaded your menu for today!"
            )
        return serializer.save(restaurant=self.request.user)


class ListMenu(ListAPIView):
    """
    Employees can only see a list of today's menus.
    Admins can filter menus by date and see the number of votes for each menu.
    """

    permission_classes = [IsEmployee]

    def get_queryset(self):
        queryset = Menu.objects.select_related("restaurant").prefetch_related(
            "votes"
        )

        if not self.request.user.is_superuser:
            return queryset.filter(created_at=datetime.date.today())

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(created_at=date)
        else:
            queryset = queryset.filter(created_at=datetime.date.today())

        return queryset.order_by("num_votes")

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return MenuListSerializer

        return MenuListSerializerEmployee


@api_view(["POST"])
def vote_for_menu(request, pk: int):
    """
    Only authenticated employees can vote and only once a day.
    A vote cannot be cancelled. Older menus cannot be voted for.
    :param request:
    :param pk:
    :return:
    """

    if not request.user.is_authenticated:
        raise NotAuthenticated()
    if not request.user.is_employee:
        raise PermissionDenied()

    menu = get_object_or_404(Menu, id=pk)
    build_version = request.headers.get("Build-Version")

    if menu.created_at != datetime.date.today():
        raise ValidationError(
            f"This menu is too old for voting. "
            f"P.S. Your build version is {build_version}"
        )

    if Vote.objects.filter(
        user=request.user, created_at=datetime.date.today()
    ):
        raise ValidationError(
            f"You have already voted today. "
            f"P.S. Your build version is {build_version}"
        )

    with transaction.atomic():
        Vote.objects.create(menu=menu, user=request.user)
        menu.num_votes += 1
        menu.save()

    return Response(
        f"Thank you for your civic awareness! "
        f"P.S. Your build version is {build_version}"
    )
