from .views import *
from django.urls import path


urlpatterns = [
    path('topics', topics_view, name="topics"),
]