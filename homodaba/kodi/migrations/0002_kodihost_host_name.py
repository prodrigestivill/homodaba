# Generated by Django 3.1 on 2021-08-11 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kodi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kodihost',
            name='host_name',
            field=models.CharField(default='', help_text='De caracter identificativo (Dormitorio, Salon...)', max_length=255, verbose_name='Nombre'),
            preserve_default=False,
        ),
    ]
