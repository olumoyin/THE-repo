from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import permissions 
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.contrib.auth import get_user_model


from academy.models import Course, StudentProfile, Lesson, Module

from users.serializers import StudentProfileSerializer 

from .permissions import IsInstructorPermission, IsInstructorPermission  

from .serializers import CourseSerializer,LessonSerializer, ModuleSerializer


class CourseViewSet(viewsets.ModelViewSet):
    '''
    Viewset for listing and creating courses
    '''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permisson_classes=[IsInstructorPermission]
    lookup_field = 'name'
    search_fields = ["name", "description"]
    
 
    
  
class ModuleViewSet(viewsets.ModelViewSet,
                    ):
    '''
    Viewset for listing and creating module

    '''
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permisson_classes=[]
    lookup_field = 'name'
    search_fields = ["name", "description"]


class LessonViewSet(viewsets.ModelViewSet
                    ):
    '''
     Viewset for listing and creating Lessons
    '''

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permisson_classes=[]
    lookup_field = 'name'
    search_fields = ["name", "description"]

 
# class QuizViewSet(viewsets.ModelViewSet):
#     '''
#     views for Quiz
#     '''













# class StudentProfileViewset(viewsets.ModelViewSet):
#     """
#     Allows List, Retrieve, Partial Update on StudentProfiles
#     List: Get all student profiles. Search by related user's "first_name", "last_name", "email".
#     Retrieve: Get a single studentprofile by profile ID.
#     Partial_update: Update profile by profile ID.
#     Delete: Allows users and admin users to delete student profiles 
#     """
#     queryset = StudentProfile.objects.all()
#     serializer_class = StudentProfileSerializer
#     # permission_classes = [permissions.IsAuthenticated]
#     search_fields = ["user__first_name", "user__last_name", "user__email"]


#     def get_queryset(self):
#         if self.request.user.is_staff or self.request.user.is_superuser:
#             return super().get_queryset()
#         # return super().get_queryset().filter(user__is_active=True)
#         return super().get_queryset().filter(user=self.request.user)
    

#     # def get_serializer_class(self):
#     #     if self.action == 'retrieve':
#     #         return StudentProfileSerializer
#     #     return super().get_serializer_class()

#     # def get_permissions(self):
#     #     if self.action in ["update", "partial_update"]:
#     #         return [
#     #             permissions.IsAuthenticated(),
#     #             custom_permissions.IsOwnerOrReadOnly(),
#     #         ]
#     #     return super().get_permissions()