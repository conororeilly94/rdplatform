# DATABASE
from __future__ import unicode_literals # Reads all languages
from django.db import models

# Create your models here.

class Main(models.Model):

    name = models.CharField(max_length=40)
    about = models.TextField()
    abouttext = models.TextField(default="")
    set_name = models.TextField(default="-")

    logourl = models.TextField(default="")
    logoname = models.TextField(default="")

    logourl2 = models.TextField(default="")
    logoname2 = models.TextField(default="")

    def __str__(self):
        
        return self.set_name + " | " + str(self.pk)