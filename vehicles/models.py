from django.db import models

from common.models import TimeStampMixin
from common.utils.uid_generator import new_uid
from stations.models import Station
from users.models import User


class Vehicle(TimeStampMixin, models.Model):
    uid = models.CharField(
        primary_key=True,
        default=new_uid,
        unique=True,
        db_index=True,
        max_length=11,
    )
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=100, blank=False)
    details = models.TextField(blank=False)
    license_plate = models.CharField(max_length=50, blank=False)
    is_available = models.BooleanField(default=True)
    is_occupied = models.BooleanField(default=False)
    occupied_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name
