from django.contrib.auth import get_user_model
from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    restaurant = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="menus"
    )
    created_at = models.DateField(auto_now_add=True)
    num_votes = models.IntegerField(default=0)

    def str(self):
        return f"{self.name}, {self.restaurant.username}, {self.created_at}"


class Vote(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="votes"
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="votes"
    )
