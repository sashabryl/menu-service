from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRestaurant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_restaurant


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_employee
