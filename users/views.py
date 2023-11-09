from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied 
from rest_framework import permissions
from users.models import BaseUserProfile, CompanyProfile, StudentProfile, User
import common.permissions as custom_permissions  
from users.serializers import BaseUserProfileSerializer, CompanyProfileSerializer, StudentProfileSerializer, UserInfoSerializer, UserRegistrationSerializer, UserSerializer

from rest_framework import generics

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    lookup_field = 'pk'
    search_fields = ["first_name", "last_name", "username"]

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        if self.action == 'retrieve':
            return UserInfoSerializer
        return super().get_serializer_class()
    
    # Define a get_permissions method that sets custom permissions based on the action    
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        if self.action == 'retrieve':
            return custom_permissions.IsOwnerOrReadOnly()  
        if self.action == 'destroy':
            return {permissions.IsAuthenticated(), permissions.IsAdminUser()}
        if self.action == 'create':
            return {permissions.AllowAny()}  
        return super().get_permissions()
    


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    '''
    Allows user retrieve and update their user profile
    '''
    serializer_class = BaseUserProfileSerializer
    #permission_classes = [custom_permissions.IsOwnerOrReadOnly]
    search_fields = ["first_name", "last_name", "user__username"]


    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            obj = get_object_or_404(BaseUserProfile, id=pk)
        except:
            obj = get_object_or_404(CompanyProfile, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_serializer(self, obj, *args, **kwargs):
        # TODO Fix "TypeError: Object of type property is not JSON serializable" error on getting company profile
        # #print("Getting serializer")
        if isinstance(self.get_object(), CompanyProfile):
            print(self.get_object())
            return CompanyProfileSerializer
        return super().get_serializer(*args, **kwargs)

class StudentProfileViewset(viewsets.ModelViewSet):
    """
    list: Get all student profiles. Search by user's "first_name", "last_name", "email".
    retrieve: Get a single profile by profile ID.
    partial_update: Update profile by profile ID.    
    """

    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    search_fields = ["user_profile__first_name", "user_profile__last_name", "user_profile__email"]


    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        #    .filter(user_profile=self.request.user.user_profile)
        return super().get_queryset()

    # Define a get_serializer_class method that 
    def get_serializer_class(self):
        if self.action == 'create':
            return ##############
        if self.action == 'retrieve':
            return ##############
        return super().get_serializer_class()


    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [
                    permissions.IsAuthenticated(), 
                    custom_permissions.IsOwnerOrReadOnly()
                    ]
        return super().get_permissions()
    




