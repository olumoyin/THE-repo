from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view, action
from rest_framework import permissions 
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.contrib.auth import get_user_model



from academy.models import (Course, StudentProfile, InstructorProfile, 
                            Lesson, Module, Answer, Enrollment,
                            Quiz, QuizQuestion)

from users.serializers import StudentProfileSerializer 
from common.permissions import IsOwnerOrReadOnly

from .permissions import IsInstructorPermission, IsStudentPermisson


from .serializers import (CourseSerializer,LessonSerializer, 
                          InstructorProfileSerializer,StudentProfileSerializer,
                          ModuleSerializer, QuizParentSerializer, AnswerSerializer,
                            QuizQuestionSerializer )


class CourseViewSet(viewsets.ModelViewSet):
    '''
    Viewset for listing and creating courses
    '''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permisson_classes=[IsInstructorPermission]
    lookup_field = 'pk'
    search_fields = ["name", "description"]

    
    def get_permissions(self):
        if self.request in ['POST','PATCH', 'PUT', 'DELETE']:
            return [IsOwnerOrReadOnly(),IsInstructorPermission()]
        return super().get_permissions()
    
    @action(detail=False,methods=['GET','POST', 'PUT', 'PATCH'])
    def by_course(self, request, *args, **kwargs):
        if request.method == 'GET':
            return super().get_queryset()
        elif request.method in ['POST', 'PUT', 'PATCH']:
            serializer =CourseSerializer(data= request.data)
            if serializer.is_valid():
                serializer.validated_data['instructor']=self.request["instructor"]
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
               

  
class ModuleViewSet(viewsets.ModelViewSet):
    '''
    Viewset for listing and creating module

    '''
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permisson_classes=[IsInstructorPermission]
    lookup_field = 'pk'
    search_fields = ["name", "description"]

  
        
    def get_permissions(self):
        
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsOwnerOrReadOnly(),IsInstructorPermission()]
        return super().get_permissions()
    

    @action(detail=False,methods=['GET','POST', 'PUT', 'PATCH'])
    def by_course(self, request, *args, **kwargs):
        if request.method == 'GET':
            course = self.request.query_params.get('course')
            if course is not None:
                modules = Module.objects.filter(course=course)
                serializer = self.get_serializer(modules, many=True)
                return Response(serializer.data)
            else:
                return Response({"error":"specify a parent course"})
        elif request.method in ['POST', 'PUT', 'PATCH']:
            serializer = ModuleSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.error, status=400)




class LessonViewSet(viewsets.ModelViewSet):
    '''
      Viewset for listing and creating Lessons
    '''

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permisson_classes=[IsInstructorPermission]
    lookup_field = 'pk'
    search_fields = ["name", "description"]

    
        
        
    def get_permissions(self):
        
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsOwnerOrReadOnly(),IsInstructorPermission()]
        return super().get_permissions()
        

    
    @action(detail=False,methods=['GET','POST','PUT', 'PATCH'])
    def by_module(self, request, *args, **kwargs):
        if request.method == 'GET':
            module = request.query_params.get('module')
            if module is not None:
                lesson = Lesson.objects.filter(module=module)
                serializer = self.get_serializer(lesson, many=True)
                return Response(serializer.data)
            else:
                return Response({"error":"specify a parent module"})
        elif request.method in ['POST', 'PUT', 'PATCH']:
            serializer = LessonSerializer(data= request.data)
            if serializer.is_valid():
                serializer.validated_data['instructor']= request.user
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

 
class QuizViewSet(viewsets.ModelViewSet):
    '''
    views for Quiz
    '''
    queryset=Quiz.objects.all()
    serializer_class = QuizParentSerializer
    lookup_field = 'pk'
    search_fields = ["name", 'lessson','course']

     
    def get_permissions(self):
        
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsOwnerOrReadOnly(),IsInstructorPermission()]
        return super().get_permissions()
    

    @action(detail=False,methods=['GET','POST', 'PUT', 'PATCH'])
    def by_lesson(self, request, *args, **kwargs):
        if request.method == 'GET':
            lesson = self.request.query_params.get('lesson')
            if lesson is not None:
                quiz = Quiz.objects.filter(lesson=lesson)
                serializer = self.get_serializer(quiz, many=True)
                return Response(serializer.data)
            else:
                return Response({"error":"specify the lesson"})
        elif request.method in ['POST', 'PUT', 'PATCH']:
            serializer = QuizParentSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.error, status=400)

             
 
class QuizQuestionViewSet(viewsets.ModelViewSet):
    '''
    views for Quiz question
    '''
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    lookup_field = 'pk' 
  
    def get_permissions(self):
            
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return {IsOwnerOrReadOnly,IsInstructorPermission}
        return super().get_permissions()
 

    @action(detail=False,methods=['GET','POST', 'PUT', 'PATCH'])
    def by_quiz(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            quiz = self.request.query_params.get('quiz')
            if quiz is not None:
                quiz = QuizQuestion.objects.filter(quiz=quiz)
                serializer = self.get_serializer(quiz, many=True)
                return Response(serializer.data)
            else:
                return Response({"error":"specify a Quiz"})
        elif request.method in ['POST', 'PUT', 'PATCH']:
            serializer = QuizQuestionSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


class AnswerviewSet(viewsets.ModelViewSet):
    queryset= Answer.objects.all()
   
    serializer_class= AnswerSerializer 
    lookup_field="pk"
    # permission_classes = [IsStudentPermisson]

    # def get_queryset(self, request, *args, **kwargs):
    #     if self.request.method == "GET":
    #         question = self.request.get_params.get('quizquestion')

    #   @action(detail=False,methods=['GET','POST', 'PUT', 'PATCH'])
    # def by_quiz(self, request, *args, **kwargs):
    #     if self.request.method == 'GET':
    #         quiz = self.request.query_params.get('question')
    #         if quiz is not None:
    #             quiz = Answer.objects.filter(quiz=quiz)
    #             serializer = self.get_serializer(quiz, many=True)
    #             return Response(serializer.data)
    #         else:
    #             return Response({"error":"specify a Quiz"})
    #     elif request.method in ['POST', 'PUT', 'PATCH']:
    #         serializer = QuizQuestionSerializer(data= request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=201)
    #         return Response(serializer.errors, status=400)


class EnrollmentViewSet(viewsets.ModelViewSet):
     
     queryset = Enrollment.objects.all()
     permissions_classes=[permissions.IsAuthenticated]

     def get_queryset(self, request, *args, **kwargs):
         user = self.request.user
         if user.is_student:
             pass
            #  enrolled = Enrollment.objects.filter(student=user)             
            #  return enrolled
         elif self.user.is_instructor:
             enrolled = Enrollment.objects.all()
             return enrolled
    
     def get_permissons(self, request, *args, **kwargs):
         user = request.user
         if user.is_student:
             return [IsOwnerOrReadOnly]
         
             
         
             


class ProfileViewSet(viewsets.ModelViewSet):
    
    lookup_field="pk"


    def get_queryset(self, request, *args, **kwargs):
        user = request.user
        if user.is_student:
            return StudentProfile
        if user.is_instructor:
            return InstructorProfile
        
    def get_permissons(self):

        user = self.request.user
        if user.is_student:
            return {IsOwnerOrReadOnly, IsStudentPermisson}
        elif user.is_instructor:
            return {IsOwnerOrReadOnly,IsInstructorPermission }
        


    def get_serializer_class(self, request, *args, **kwargs):
        user = request.user
        if user.is_student:
            return [StudentProfileSerializer]
        if user.is_instructor:
            return [InstructorProfileSerializer]

















