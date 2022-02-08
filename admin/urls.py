from django.urls import path

from admin.views import index_view

urlpatterns = [
    path('', index_view, name='index'),
]
