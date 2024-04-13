from django.db import models


class GanoConCocaCola(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    telefono = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Gano con Coca Cola Lead'
        verbose_name_plural = 'Gano con Coca Cola Leads'