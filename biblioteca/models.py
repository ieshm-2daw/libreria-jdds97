from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator,MinValueValidator

class Usuario(AbstractUser):
    dni=models.CharField(max_length=10,unique=True)
    direccion=models.CharField( max_length=200)
    telefono=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(9)],null=True)
    def __str__(self):
        return self.username
    
class Libro(models.Model):
    titulo=models.CharField(max_length=200)
    autor=models.ManyToManyField("Autor" ,blank=True)
    editorial=models.ForeignKey("Editorial",on_delete=models.CASCADE,blank=True,null=True)
    fecha_publicacion=models.DateField()
    rating= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    genero=models.CharField(max_length=100)
    ISBN=models.CharField(max_length=13)
    resumen=models.TextField()
    DISPONIBILIDAD_CHOICES=(
        ('D','Disponible'),
        ('P','Prestado'),
        ('R','Reservado'),
    )
    disponibilidad=models.CharField(max_length=20,choices=DISPONIBILIDAD_CHOICES,default='D')
    portada=models.ImageField(upload_to='portadas/',null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    def __str__(self):
        return self.titulo
class Autor(models.Model):
    nombre=models.CharField(max_length=100)
    biografia=models.TextField()
    foto=models.ImageField(upload_to='autores/',null=True,blank=True)
    def __str__(self):
        return self.nombre
class Editorial(models.Model):
    nombre=models.CharField(max_length=100)
    direccion=models.CharField( max_length=200)
    sitio_web=models.URLField()
    def __str__(self):
        return self.nombre
class Prestamo(models.Model):
    libro=models.ForeignKey("Libro",on_delete=models.CASCADE)
    usuario=models.ForeignKey("Usuario",on_delete=models.CASCADE)
    fecha_prestamo=models.DateField()
    fecha_devolucion=models.DateField(null=True,blank=True)
    ESTADOS_CHOICES=(
        ('P','Prestado'),
        ('D','Devuelto'),
    )
    estado=models.CharField(max_length=20,choices=ESTADOS_CHOICES,default='P')
    def __str__(self):
        return self.libro