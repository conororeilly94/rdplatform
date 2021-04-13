# DATABASE
from __future__ import unicode_literals # Reads all languages
from django.db import models

# Create your models here.

class ContactForm(models.Model):

    name = models.CharField(max_length=40)
    email = models.CharField(max_length=60)
    text = models.TextField()
    date = models.CharField(max_length=12, default="")
    time = models.CharField(max_length=12, default="")

    def __str__(self):
        
        return self.name