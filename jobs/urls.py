from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="jobs_home"),
    # path('<int:course_id>/') 
]