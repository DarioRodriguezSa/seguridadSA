from django.contrib.auth.models import User
from Apps.projects.models import Project
from django.db import models

class Userdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    debts = models.FloatField(default=0, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='users')


class Pago(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.CharField(max_length=255, blank=True, null=True)
    proyecto = models.CharField(max_length=255, blank=True, null=True)