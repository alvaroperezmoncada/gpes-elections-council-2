import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # project_name nombre del proyecto
django.setup()

import pandas as pd
from council_member.models import CouncilMember

df = pd.read_csv('Datos Consejo.csv', sep=',')
for i in df.index:
    email = df['Correo electrónico'][i]
    member, created = CouncilMember.objects.get_or_create(email=email)
    if created:
        member.firstname = df['Nombre'][i]
        member.lastname = df['Apellidos'][i]
        member.dni_number = df['DNI'][i]
        member.save()

