from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):

    class Meta:
        ordering = ('id',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')
