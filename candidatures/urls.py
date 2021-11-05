from django.urls import path

from admin.views import index_view
from candidatures.views import presentation60_view

urlpatterns = [
    path('', presentation60_view),
]
