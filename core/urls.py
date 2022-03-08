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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from admin.views import commision60, edit_candidate60, commision15, edit_candidate15, vote60, send_pass60, ballot60, \
    register_vote60, results60, selector60, selector15, results15, vote15, send_pass15, ballot15, register_vote15
from candidatures.views import presentation60_view, confirm60_view, ok60, presentation15_view, confirm15_view, ok15, \
    allegation60, allegation15, allegate, allegation_ok, view_candidatures60, view_candidatures15, \
    view_candidate_details
from core import settings

urlpatterns = [
    path('', include('admin.urls')),
    path('presentacion_60', presentation60_view, name='presentation60'),
    path('presentacion_15', presentation15_view, name='presentation15'),
    path('confirmar_60', confirm60_view, name='confirm60'),
    path('confirmar_15', confirm15_view, name='confirm15'),
    path('ok_60', ok60, name='ok60'),
    path('ok_15', ok15, name='ok15'),
    path('alegaciones_60', allegation60, name='allegation60'),
    path('alegaciones_15', allegation15, name='allegation15'),
    path('ver_candidaturas_60/', view_candidatures60, name='candidatures60'),
    path('ver_candidaturas_15/', view_candidatures15, name='candidatures15'),
    path('ver_candidaturas/<int:num>', view_candidate_details, name='candidate-details'),
    path('alegacion_ok/', allegation_ok),
    path('alegar/<int:num>/', allegate, name='allegate'),
    path('comision_60/', commision60, name='commision60'),
    path('comision_60/<int:num>/', edit_candidate60, name='candidate-edit60'),
    path('comision_15/', commision15, name='commision15'),
    path('comision_15/<int:num>/', edit_candidate15, name='candidate-edit15'),
    path('votacion_60/', vote60),
    path('votacion_15/', vote15),
    path('envia_clave_60/', send_pass60),
    path('envia_clave_15/', send_pass15),
    path('papeleta_60/<int:ca>/', ballot60, name='ballot60'),
    path('papeleta_15/<int:ca>/', ballot15, name='ballot15'),
    path('papeleta_60/<int:ca>/registrar/', register_vote60),
    path('papeleta_15/<int:ca>/registrar/', register_vote15),
    path('resultados_60/', results60, name='results60'),
    path('resultados_15/', results15, name='results15'),
    path('admin/', admin.site.urls),
    path('authenticate/', include('authenticate.urls')),

    path('gpes/60/recuento/', selector60, name='recuento60'),
    path('gpes/15/recuento/', selector15, name='recuento15'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
