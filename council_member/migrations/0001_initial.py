# Generated by Django 3.2.8 on 2021-11-04 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('circumscription', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CouncilMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Esta activo')),
                ('voting_date', models.DateTimeField(null=True, verbose_name='Fecha de votación')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='council_member_district_set', to='circumscription.circumscription', verbose_name='Circunscripción')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='council_member_user_set', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Miembro del consejo',
                'verbose_name_plural': 'Miembros del consejo',
            },
        ),
    ]
