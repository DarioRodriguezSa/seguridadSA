# Generated by Django 4.2.6 on 2023-10-12 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_costo'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
