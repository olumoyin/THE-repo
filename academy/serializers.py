from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import (Course, CourseReview , 
                    Module, Lesson, Enrollment, 
                    Quiz, QuizQuestion, Answer, Tag)

from users.models import  StudentProfile, InstructorProfile




class EnrowmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "student",
            " enrollment_date",
            "progress"            
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    enrollment = EnrowmentSerializer(read_only=True)
    student_fullname = serializers.SerializerMethodField(read_only=True)
    
   
    class Meta: 
        model = StudentProfile
        fields = [
            "id",
            # "user",
            "student_fullname",
            'user_profile',
            "bio",
            "enrollment"
        ]

    def get_student_fullname(self, obj):
        return obj.student_fullname()

class InstructorProfileSerializer(serializers.ModelSerializer):

    class Meta: 
        model = InstructorProfile
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    instructor_fullname = serializers.CharField(source='get_instructor_fullname' ,read_only=True)
    course_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'cover_image',
            'course_url',
            'description',
            'difficulty',
            'instructor',
            'instructor_fullname',
            'summary',
            'prerequisites',
            'requirements',
            'is_certified',
            'schedule',
            'duration',
            'average_rating',
            'price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'average_rating',
            'created_at',
            'updated_at',
            'id',
            'course_url',
            ]
        
    def get_course_url(self, obj):
            request = self.context.get('request')
            if request is None:
                return None
            return reverse("course-detail",kwargs={"pk":obj.pk}, request=request)
    
 

class ModuleSerializer(serializers.ModelSerializer):
    module_url = serializers.SerializerMethodField(read_only=True)
    course_info = CourseSerializer(read_only=True)
    # i need 
#         
    class Meta:
        model= Module
   
        fields= [
            'id',
            'name',
            "module_url",
           'course',
           'course_info',
        #    'parentcourse',
           'description',
           'thumbnail',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'module_url',
             'created_at',
            'updated_at',
        ]
        
    def get_module_url(self, obj):
            request = self.context.get('request')
            if request is None:
                return None
            return reverse("module-detail",kwargs={"pk":obj.pk}, request=request)

    

class LessonSerializer(serializers.ModelSerializer):
    lesson_url = serializers.SerializerMethodField(read_only=True)
    # module = ModuleSerializer(read_only=True)
    
#         
    class Meta:
        model= Lesson
        fields= [
            'id',
            'name',
            'description',
            'module',
            'video_url',
            'lesson_video',
            'lesson_documents',
            'audio_url',
            'note',
            'lesson_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
             'created_at',
            'updated_at'
        ]

    def get_lesson_url(self, obj):
            request = self.context.get('request')
            if request is None:
                return None
            return reverse("lesson-detail",kwargs={"pk":obj.pk}, request=request)


#     def get_instructor(self, obj):
#          if not hasattr(obj, 'instructor'):
#              return None
#          return obj.instructor.instructor_fullname
    
class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "student",
            "enrollment_date",
            "progress"
        ]
        read_only_fields=[
            "student"
        ]

  


class QuizParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = [
            "id",
            "name",
            "lesson",
          ]
        
class QuizQuestionSerializer(serializers.ModelSerializer):
   
    parentQuiz = QuizParentSerializer(read_only=True) 

    class Meta:
        model = QuizQuestion
        fields = [
            "id",
            "quiz",
            "question",
            "hint",
            "correct_answer",
            "options",
            "answer_text",
            'url_submission',
            'parentQuiz'            
        ]   
        extra_kwargs = {
             'correct_answer':{'write_only':True},
        }
        write_only_fields = [
            "correct_answer"
        ]

class AnswerSerializer(serializers.ModelSerializer):
     question = QuizQuestionSerializer(read_only=True) 

     class Meta:
        model=Answer
        fields=[
            "id",
            "selected_option",
            "input_text",
            "url_submisson",
            "question"
        ]
    

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tag
        fields="__all__"


class CourseReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=CourseReview
        fields="__all__"

        read_only_fields = ["author"]

        def save(self, *args, **kwargs):

            author = self.validated_data.get('author', self.context['request'].user)
            self.save()
            super().save( *args, **kwargs)
    