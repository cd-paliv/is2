# Generated by Django 4.1.7 on 2023-03-23 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OMDApp', '0005_alter_perro_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('Cliente', 'Correspondiente al rol de Cliente en la documentación')]},
        ),
        migrations.CreateModel(
            name='Veterinario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('Veterinario', 'Correspondiente al rol de Veterinario en la documentación')],
            },
        ),
    ]
