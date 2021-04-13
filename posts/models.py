# DATABASE
from __future__ import unicode_literals # Reads all languages
from django.db import models

# Create your models here.

class Posts(models.Model):

    name = models.CharField(max_length=250)
    short_txt = models.TextField()
    body_txt = models.TextField()
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=12, default = "00:00")
    img = models.TextField()
    imgurl = models.TextField(default="-")
    author = models.CharField(max_length=50)
    catname = models.CharField(max_length=50, default='-')
    catid = models.IntegerField(default=0)    
    ocatid = models.IntegerField(default=0) # Orig Category ID
    views = models.IntegerField(default=0)
    tag = models.TextField(default='')
    act = models.IntegerField(default=0)
    rand = models.IntegerField(default=0)

    def __str__(self):
        
        return self.name