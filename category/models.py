# DATABASE
from __future__ import unicode_literals # Reads all languages
from django.db import models

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    

    def __str__(self):
        
        return self.name