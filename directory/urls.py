
from django.urls import path
from . import views





urlpatterns = [
    path('service-locations', views.ServiceLocationList.as_view(), name="service-locations-list"),
    path('service-locations/create', views.ServiceLocationCreateView.as_view(), name="create-service-locations"),
]