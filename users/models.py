from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    nickname    = models.CharField(max_length=30, null=True)
    kakao       = models.CharField(max_length=30, null=True)
    naver       = models.CharField(max_length=30, null=True)
    image       = models.URLField(max_length=2000, null=True)
    name        = models.CharField(max_length=30, null=True)
    age         = models.IntegerField(null=True)
    description = models.CharField(max_length=2000, null=True)
    namecard    = models.TextField(max_length=3000, null=True)

    class Meta:
        db_table = 'users'