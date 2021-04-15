from django.db import models

# Create your models here.
class Devoir(models.Model):
    name=models.CharField(max_length=50)
    file_dev=models.FileField(upload_to='files')
