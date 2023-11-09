from .views import *
from django.urls import path


urlpatterns = [
    path('complaint-tickets', ticketing_view, name="topics"),
]