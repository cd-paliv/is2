# Generated by Django 4.1.7 on 2023-03-22 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OMDApp', '0004_alter_perro_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perro',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]