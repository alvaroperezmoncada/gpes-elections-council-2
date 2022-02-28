import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # project_name nombre del proyecto
django.setup()

import pandas as pd
from council_member.models import CouncilMember

df = pd.read_csv('Censo_Consejo_2021_5.csv', sep=';')
for i in df.index:
    body = {
        'firstname': df['firstname'][i],
        'lastname': df['lastname'][i],
        'email': df['email'][i]
    }
    member = CouncilMember.objects.create(**body)

