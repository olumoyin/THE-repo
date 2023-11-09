from django.urls import path
from .views import StudentProfileViewset, UserProfileDetailView, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()

# List & Retrieves
router.register('users', UserViewSet, basename='users')


urlpatterns = [

    # JWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profiles
    path('profile/<str:pk>/', UserProfileDetailView.as_view(),  name='profile-detail'),
    

] + router.urls