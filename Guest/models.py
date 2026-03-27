from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students/')
