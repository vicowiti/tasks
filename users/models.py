from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        MEMBER = "MEMBER", "Member"
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.MEMBER)
    has_default_password = models.BooleanField(default=True)

    def is_admin(self):
        return self.role == self.Roles.ADMIN

    def is_manager(self):
        return self.role == self.Roles.MANAGER
    

    def is_member(self):
        return self.role == self.Roles.MEMBER