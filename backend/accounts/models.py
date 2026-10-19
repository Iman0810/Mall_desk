from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class StoreMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN" , "Administrator"
        MANAGER = "MANAGER" , "Store Manager"
        STAFF = "STAFF" , "Staff Member"

    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "memberships")

    store = models.ForeignKey("stores.Store", on_delete = models.CASCADE, related_name = "memberships")
    role = models.CharField(max_length=20, choices=Role.choices)

    class Meta:
        unique_together = ("user", "store")

    def __str__(self):
        return f"{self.user.username} - {self.store.name} ({self.role})"