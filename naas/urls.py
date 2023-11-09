from .views import *
from django.urls import path


urlpatterns = [
    path('service-requests', service_requests_view, name="topics"),
]