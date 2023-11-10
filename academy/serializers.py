from rest_framework import serializers

from .models import Course , Module, Lesson, Enrollment, Quiz, QuizQuestion, QuizQuestionOption

from users.models import  StudentProfile, InstructorProfile


# class CourseSerializer(serializers.ModelSerializer):
#     instructor = serializers.SerializerMethodField(read_only=True, )
    
    # class Meta:
    #     model= Course
    #     fields= (
    #         'id',
    #         'name',
    #         'cover_image',
    #         'description',
    #         'difficulty',
    #         'summary',
    #         'price',
    #     #     'instructor',
    #         'prerequisites',
    #         'requirements',
    #         'is_certified',
    #         'schedule',
    #         'duration',
    #         'average_rating',
    #         'created_at',
    #         'updated_at',
    #     )

#     def get_instructor(self, obj):
#          if not hasattr(obj, 'instructor'):
#              return None
#          return obj.instructor.instructor_fullname
    
class CourseSerializer(serializers.ModelSerializer):
    instructor_fullname = serializers.CharField(source='get_instructor_fullname' ,read_only=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = [
            'average_rating',
            'created_at',
            'updated_at',
            'id',
            ]


class ModuleSerializer(serializers.ModelSerializer):
#         
    class Meta:
        model= Module
        fields= (
            'id',
            'student'
        #     'instructor',
           'course',
           'enrollment',
           'progress'
            'created_at',
            'updated_at',
        )

#     def get_instructor(self, obj):
#          if not hasattr(obj, 'instructor'):
#              return None
#          return obj.instructor.instructor_fullname
    

class LessonSerializer(serializers.ModelSerializer):
    
#         
    class Meta:
        model= Module
        fields= (
            "id",
            'name',
            'description',
            "participant",
            'description',
            'course',
            'module',
            'video_url'
            'lesson_url',
            'lesson_documents',
            "audio_url"
            "note",
        #     'instructor',           
            'created_at',
            'updated_at',

        )

#     def get_instructor(self, obj):
#          if not hasattr(obj, 'instructor'):
#              return None
#          return obj.instructor.instructor_fullname
    
class EnrowmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "student",
            " enrollment_date",
            "progress"
            ""
        ]

class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "student",
            " enrollment_date",
            "progress"
            ""
        ]