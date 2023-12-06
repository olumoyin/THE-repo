from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view, action
from rest_framework import permissions , generics
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.contrib.auth import get_user_model



from academy.models import (Course,Lesson, Module, 
                            Answer, Enrollment,Tag,
                            Quiz, QuizQuestion, CourseReview)

from users.serializers import StudentProfileSerializer 
from users.models import BaseUserProfile, StudentProfile, InstructorProfile

from common.permissions import IsOwnerOrReadOnly

from .permissions import IsInstructorPermission, IsStudentPermisson


from .serializers import (CourseSerializer,LessonSerializer, 
                          InstructorProfileSerializer,StudentProfileSerializer,
                          ModuleSerializer, QuizParentSerializer, AnswerSerializer,
                            QuizQuestionSerializer, EnrollmentSerializer, 
                            TagSerializer, CourseReviewSerializer)


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
    #         return Response(serializer.errors, s tatus=400)


class EnrollmentViewSet(viewsets.ModelViewSet):
     

     """
     A class for enrollments 
     -Enrolls a course (only students can)
     """
     
     #queryset gets only the users enrollwed courses
     queryset = Enrollment.objects.all()
     serializer_class =EnrollmentSerializer
     permission_classes=[IsOwnerOrReadOnly]

     

     def get_queryset(self, *args, **kwargs):

        user = self.request.user       
        return Enrollment.objects.filter(student=user.id)
     
     
     def get_permissions(self):
         if self.request.method == 'GET':
             return [IsOwnerOrReadOnly()]
         if self.request.method in ['GET','POST', 'PUT', 'PATCH']:
            return [IsStudentPermisson()]
         if self.request.method in ['DELETE']:
            return [IsOwnerOrReadOnly(),IsStudentPermisson()]
     
     

     def perform_create(self, serializer):
        user = self.request.user
        studentprofile = StudentProfile.objects.filter(user_profile=user)
        serializer.save(student=studentprofile)


     @action(detail=False,methods=['GET','POST', 'PUT', 'PATCH'])
     def by_course(self, request, *args, **kwargs):
        if request.method == 'GET':
            course = self.request.query_params.get('course')
            if course is not None:
                review = Enrollment.objects.filter(course=course)
                serializer = self.get_serializer(review, many=True)
                return Response(serializer.data)
            else:
                return Response({"error":"specify a parent course"})
        elif request.method in ['POST', 'PUT', 'PATCH']:
            serializer = EnrollmentSerializer(data = request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save(author = request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)



    

class StudentProfileViewSet(viewsets.ModelViewSet):

    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    lookup_field="pk"
     

    def get_permissons(self):

        if self.request.method == 'GET':
            return [IsOwnerOrReadOnly]
        if self.request.method == 'POST':
                return [IsStudentPermisson]
        if self.request.method in ['PATCH','DELETE','UPDATE']:
            return [IsOwnerOrReadOnly,IsStudentPermisson]


class InstructorProfileViewSet(viewsets.ModelViewSet):

    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    lookup_field="pk"
     

    def get_permissons(self):

        if self.request.method == 'GET':
            return [IsOwnerOrReadOnly]
        if self.request.method == 'POST':
                return [IsInstructorPermission]
        if self.request.method in ['PATCH','DELETE','UPDATE']:
            return [IsOwnerOrReadOnly,IsInstructorPermission]



class CourseSearchView(generics.ListAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self, *args, **kwargs):
        '''
        define qs(as inherited queryset)
        q is equal to the params        
        '''
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            results = qs.search(q)
            return results
        return qs



class TagViewSet(ModuleViewSet):
    '''
    The tag  class 
    -to create, delete, list and retieve tags
    '''

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CourseReviewViewSet(ModuleViewSet):

    '''
    Reviews for each course
    '''
        
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer



    def get_permissions(self):

        if self.request.method == 'GET':
                    return [IsOwnerOrReadOnly()]
        if self.request.method in ['POST','PATCH','DELETE','UPDATE']:
                return [IsStudentPermisson()]
    


    @action(detail=False,methods=['GET','POST', 'PUT', 'PATCH'])
    def by_course(self, request, *args, **kwargs):
        if request.method == 'GET':
            course = self.request.query_params.get('course')
            if course is not None:
                review = CourseReview.objects.filter(course=course)
                serializer = self.get_serializer(review, many=True)
                return Response(serializer.data)
            else:
                return Response({"error":"specify a parent course"})
        elif request.method in ['POST', 'PUT', 'PATCH']:
            serializer = CourseReviewSerializer(data = request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save(author = request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


        









