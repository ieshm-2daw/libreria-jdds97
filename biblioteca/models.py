from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator 

class Usuario(AbstractUser):
    dni=models.CharField(max_length=9)
    direccion=models.TextField()
    telefono=models.IntegerField(validators=[MaxValueValidator(9)])
class Libro(models.Model):
    título=models.TextField()