from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.CourseViewSet, basename="course")


urlpatterns = [
    path('courses/',include(router.urls))
] + router.urls