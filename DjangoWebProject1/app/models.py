"""
Definition of models.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    initiator_uuid = models.CharField(max_length=64, blank=True, null=True)
    is_seach = models.BooleanField(default=False)  # Галочка для пользователя
# Create your models here.
