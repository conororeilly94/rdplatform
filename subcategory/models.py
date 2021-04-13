# DATABASE
from __future__ import unicode_literals # Reads all languages
from django.db import models

# Create your models here.

class SubCategory(models.Model):

    name = models.CharField(max_length=50)
    catname = models.CharField(max_length=50)
    catid = models.IntegerField()
    

    def __str__(self):
        
        return self.name