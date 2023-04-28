from django.db import models
from django.utils import timezone


# Create your models here.


class SaveImage(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    file = models.ImageField(upload_to="images")
    create_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=0)


class VisitTrace(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    ip = models.CharField(max_length=255)
    useragent = models.CharField(max_length=255)
    referer = models.CharField(max_length=255)
