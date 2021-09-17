from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    nickname  = models.CharField(max_length=30, null=True)
    kakao     = models.CharField(max_length=30, null=True)
    naver     = models.CharField(max_length=30, null=True)
    image     = models.URLField(max_length=2000, null=True)
    name      = models.CharField(max_length=30, null=True)
    slogan    = models.CharField(max_length=2000, null=True)
    introduce = models.TextField(max_length=3000, null=True)
    email     = models.CharField(max_length=200, null=True)
    location  = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'users'

class History(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    year     = models.IntegerField(null=True)
    title    = models.CharField(max_length=300, null=True)
    subtitle = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'histories'