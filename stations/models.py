from django.db import models

from common.models import TimeStampMixin
from common.utils.uid_generator import new_uid


class Station(TimeStampMixin, models.Model):
    uid = models.CharField(
        max_length=11, primary_key=True, default=new_uid, db_index=True, unique=True
    )
    name = models.CharField(max_length=100, blank=False)
    address = models.TextField(blank=False)
    location = models.JSONField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
