from django.db import models

# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to='images/')
    font = models.CharField(max_length=250)