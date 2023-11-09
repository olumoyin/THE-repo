from django.contrib import admin

from academy.models import (
    Course, 
    Enrollment,
    InstructorProfile,
    # InstructorReview,
    Module,
    StudentProfile, 
    Tag,
    Lesson,
    # TagModule,
    # CourseReview,
    Quiz,
    QuizQuestion,
    QuizQuestionOption
)



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name",  "difficulty", "updated_at")
    list_filter = ( "difficulty", "schedule")
    search_fields = ( "name",)

# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = ["student", "course", "enrollment_date"]
#     list_filter = ["student", "course", "enrollment_date"]
#     search_field = ["student", "course"]

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name',]
#     list_filter = ['name']
#     search_fields = ['name',]


# @admin.register(Module)
# class ModuleAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'course', 'created_at']
#     list_filter = ['course', 'updated_at' ]
#     search_fields = ['name', 'description']
#     autocomplete_fields = ['tags']

# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'module', 'updated_at']
#     list_filter = ['module', 'created_at', 'updated_at']
#     search_fields = ['name', 'description']


# @admin.register(TagModule)
# class TagModuleAdmin(admin.ModelAdmin):
#     list_display = ['id', 'tag', 'module']
#     list_filter = ['tag', 'module']
#     search_fields = ['module']


# @admin.register(CourseReview)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['author', 'course', 'rating', 'comment', ]
#     list_filter = ['rating', 'course', 'created_at']
#     search_fields = ['name', 'comment']

# @admin.register(Quiz)
# class QuizAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'lesson', 'updated_at', ]
#     list_filter = ['updated_at']
#     search_fields = ['name']

# @admin.register(QuizQuestion)
# class QuizQuestionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'quiz', 'body', 'has_options', ]
#     list_filter = ['has_options']
#     search_fields = ['body', "hint"]


# @admin.register(QuizQuestionOption)
# class QuizQuestionOptionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'question', 'option_text']
#     list_filter = ['question']
#     search_fields = ['option_text']



# @admin.register(StudentProfile)
# class StudentProfileAdmin(admin.ModelAdmin):
#     list_display  =  ["id", "user"]
#     list_filter   =  ["user"]
#     search_fields =  ["user"]

# @admin.register(InstructorProfile)
# class InstructorProfileAdmin(admin.ModelAdmin):
#     list_display  =  ["id", "user"]
#     list_filter   =  ["user",]
#     search_fields =  ["user", "linkedin_url"]


# @admin.register(InstructorReview)
# class InstructorReviewAdmin(admin.ModelAdmin):
#     list_display  =  ["id", "author", "instructor", "rating", "updated_at"]
#     list_filter   =  ["rating", "author", "instructor"]
#     search_fields =  ["comment", "author", "instructor"]