"""core- URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from admin.views import commision60, edit_candidate60, commision15, edit_candidate15, vote60, send_pass60, ballot60, \
    register_vote60
from candidatures.views import presentation60_view, confirm60_view, ok60, presentation15_view, confirm15_view, ok15, \
    allegation60, allegation15, allegate, allegation_ok, view_candidatures60, view_candidatures15

urlpatterns = [
    path('', include('admin.urls')),
    path('presentacion_60', presentation60_view),
    path('presentacion_15', presentation15_view),
    path('confirmar_60', confirm60_view),
    path('confirmar_15', confirm15_view),
    path('ok_60', ok60),
    path('ok_15', ok15),
    path('alegaciones_60', allegation60),
    path('alegaciones_15', allegation15),
    path('ver_candidaturas_60/', view_candidatures60),
    path('ver_candidaturas_15/', view_candidatures15),
    path('alegacion_ok/', allegation_ok),
    path('alegar/<int:num>/', allegate),
    path('comision_60/', commision60),
    path('comision_60/<int:num>/', edit_candidate60),
    path('comision_15/', commision15),
    path('comision_15/<int:num>/', edit_candidate15),
    path('votacion_60/', vote60),
    path('envia_clave_60/', send_pass60),
    path('papeleta_60/<int:ca>/', ballot60),
    path('papeleta_60/<int:ca>/registrar/', register_vote60),
    path('admin/', admin.site.urls),
    path('authenticate/', include('authenticate.urls')),
]
