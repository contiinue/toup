from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class AuthHH(models.Model):
    access_token = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=128)


class User(AbstractUser):
    auth_hh = models.OneToOneField(AuthHH, on_delete=models.CASCADE, null=True)
    resume_id = models.CharField(max_length=128)
    covering_letter = models.TextField()
    telegram_id = models.CharField(max_length=63)
    query_text = models.CharField(max_length=63)

    class Meta:
        ordering = ("id",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")
