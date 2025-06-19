"""
Definition of models.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    initiator_uuid = models.CharField(max_length=64, blank=True, null=True)
    initiator_code = models.CharField(max_length=64, blank=True, null=True)
    Client_uuid = models.CharField(max_length=64, blank=True, null=True)
    is_seach = models.BooleanField(default=False)
    preferredTheme = models.CharField(max_length=64, blank=True, null=True)

class Usermanual(models.Model):
    title = models.CharField("Header", max_length=255)
    content = models.TextField("Text Sate")
    created_at = models.DateTimeField("Date create", auto_now_add=True)
    def __str__(self):
        return self.title

class Advertisement(models.Model):
    title = models.CharField("Header", max_length=255)
    content = models.TextField("Text Sate")
    created_at = models.DateTimeField("Date create", auto_now_add=True)
    def __str__(self):
        return self.title

class GlobalSettings(models.Model):
    URL_ITILIUM = models.URLField("URL ITILIUM", default="http://example.com")
    usernameAPI = models.CharField("Username API", max_length=100, default="user")
    passwordAPI = models.CharField("Passowd API", max_length=100, default="password")

    def __str__(self):
        return "Settings ITILIUM API" 

    def save(self, *args, **kwargs):
        self.pk = 1  
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj