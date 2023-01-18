from django.db import models

from common.models import TimeStampMixin
from common.utils.uid_generator import new_uid


class Otp(TimeStampMixin, models.Model):
    uid = models.CharField(
        max_length=11, unique=True, primary_key=True, default=new_uid, db_index=True
    )
    otp = models.IntegerField(blank=False)
    email = models.EmailField(blank=False)
    expiry_at = models.DateTimeField(blank=False)
    is_expired = models.BooleanField(default=False)
