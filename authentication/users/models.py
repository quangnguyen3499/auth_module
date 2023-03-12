import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import BasePermission


class Company(models.Model):
    class Types(models.TextChoices):
        PORTFOLIO = "PORTFOLIO", "Portfolio"
        NONPORTFOLIO = "NONPORTFOLIO", "NonPortfolio"
    
    name = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=50, choices=Types.choices, null=True, blank=True)


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEAM = "TEAM", "Team"
        FOUNDER = "FOUNDER", "Founder"
        PARTNERSHIP = "PARTNERSHIP", "Partnership"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        DEACTIVATED = "DEACTIVATED", "Deactivated"

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    role = models.CharField(max_length=50, choices=Roles.choices, null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    active_expires_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    updated_date = models.DateTimeField(auto_now=True, max_length=(6))
    created_date = models.DateTimeField(auto_now_add=True, max_length=(6))

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_team(self):
        return self.role == self.Roles.TEAM

    @property
    def is_founder(self):
        return self.role == self.Roles.FOUNDER

    @property
    def is_partnership(self):
        return self.role == self.Roles.PARTNERSHIP


class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="team")


class Founder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="founder")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="founder")


class Partnership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="partnership")


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True
        token = request.auth.decode("utf-8")
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
