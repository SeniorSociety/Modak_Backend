from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name  = models.CharField(max_length=30)
    image = models.URLField(max_length=2000)
    kakao = models.CharField(max_length=30)
    naver = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'