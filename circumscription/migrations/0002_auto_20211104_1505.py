# Generated by Django 3.2.8 on 2021-11-04 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circumscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circumscription',
            name='cod_ine',
            field=models.CharField(max_length=2, verbose_name='Cod. ine'),
        ),
        migrations.AlterField(
            model_name='circumscription',
            name='order',
            field=models.IntegerField(verbose_name='Orden'),
        ),
        migrations.AlterField(
            model_name='circumscription',
            name='places',
            field=models.IntegerField(verbose_name='Puestos'),
        ),
    ]
