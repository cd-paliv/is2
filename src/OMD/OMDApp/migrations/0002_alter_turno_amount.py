# Generated by Django 4.1.7 on 2023-05-16 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OMDApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
