# Generated by Django 3.2.8 on 2021-11-11 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidatures', '0002_auto_20211111_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidature',
            name='is_adult',
            field=models.BooleanField(default=False, verbose_name='¿Es mayor de edad?'),
        ),
        migrations.AlterField(
            model_name='candidature',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='Validada por la Comisión Electoral'),
        ),
        migrations.AlterField(
            model_name='candidature',
            name='validated_circumscription',
            field=models.BooleanField(default=False, verbose_name='Circunscripción correcta'),
        ),
    ]
