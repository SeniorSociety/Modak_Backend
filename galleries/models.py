from django.db import models

from core.models import TimeStampModel

class Gallery(models.Model):
    name  = models.CharField(max_length=30)
    image = models.URLField(max_length=2000)
    bookmark = models.ManyToManyField('users.user', related_name='bookmarkers')

    class Meta:
        db_table = 'galleries'

class Posting(TimeStampModel):
    gallery    = models.ForeignKey('gallery', on_delete=models.CASCADE)
    title      = models.CharField(max_length=100)
    content    = models.CharField(max_length=2000)
    user       = models.ForeignKey('users.user', on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    thumbnail  = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'postings'

class Comment(TimeStampModel):
    user    = models.ForeignKey('users.user', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    posting = models.ForeignKey('posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'