from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from .mymanager import UserManager


class CustomUser(AbstractUser):
    Phone_number = models.CharField(max_length=15, unique=True)
    Phone_is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)

    USERNAME_FIELD = "Phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()
