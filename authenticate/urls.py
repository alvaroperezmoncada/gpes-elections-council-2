from django.urls import path

from authenticate.views import login

urlpatterns = [
    path('login', login),
]
