"""
Definition of models.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    initiator_uuid = models.CharField(max_length=64, blank=True, null=True)
# Create your models here.
