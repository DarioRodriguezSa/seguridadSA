from django.db import models


class Project(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_finalizacion_estimada = models.DateField()
    costo = models.FloatField(default=0, blank=True, null=True)
    user_total = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    


