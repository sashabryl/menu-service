from rest_framework.permissions import BasePermission


class IsRestaurant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_restaurant
        )


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_employee or
            request.user.is_superuser
        )
