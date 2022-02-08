from django.contrib.auth import views
from django.urls import path

from authenticate.forms import CustomAuthForm

urlpatterns = [
    path('login/', views.LoginView.as_view(authentication_form=CustomAuthForm), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
