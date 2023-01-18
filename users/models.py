from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager
from common.models import TimeStampMixin
from common.utils.uid_generator import new_uid
from common.utils.enums import USER_ROLES


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):
    uid = models.CharField(
        primary_key=True,
        default=new_uid,
        unique=True,
        db_index=True,
        max_length=11,
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, choices=[(role.name, role.value) for role in USER_ROLES]
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
