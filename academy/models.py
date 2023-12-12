import contextlib
from django.db import models
from django.db.models.query import QuerySet
from shortuuid.django_fields import ShortUUIDField
from users.models import BaseUserProfile, InstructorProfile, StudentProfile
from wta_api_build import settings 
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
import uuid

from django.db.models import Q



class CourseQueryset(models.QuerySet):
    '''
    creating a query set for simplification of searchs
    '''

    def search(self, query):
        #checks the look up and filters the model
        lookup = Q(summary__icontains=query) | Q(name__icontains=query) | Q(description_icontains = query)
        qs = self.filter(lookup)
        return qs


class CourseManager(models.Manager):
    '''
    creating a query set for simplification of searchs
    '''

    def get_queryset(self) -> QuerySet:
        # overides the initial queryset and creates a custom query set based on the input 
        return CourseQueryset(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)




class Course(models.Model): 
    DIFFICULTY = (
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced")
    )
    SCHEDULE = (
        ("Self Paced", "Self Paced"),
        ("Tutor Paced", "Tutor Paced")
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    cover_image = models.ImageField(upload_to='academy/courses/cover_images', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY, null=True, blank=True)
    summary = models.TextField( null=True, blank=True)
    price= models.FloatField(null=True, blank=True)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name="instructor",null=True)
    prerequisites = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    is_certified = models.BooleanField(default=False)
    schedule = models.CharField(max_length=20, choices=SCHEDULE, null=True, blank=True)
    duration = models.CharField(max_length=30, null=True, blank=True)
    average_rating = models.FloatField(default=0)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    objects = CourseManager()

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.name
  
    def get_instructor_fullname(self):
        return '' if not self.instructor else self.instructor.instructor_fullname()


class CourseReview(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name="review_author")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(validators=[
                                                     MinValueValidator(0), 
                                                     MaxValueValidator(5)
                                                    ]
                                        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("author", "course")
        ordering = ["updated_at"]
        
    def __str__(self):
        return f"Comment by {self.user.email} on {self.course.name}"    



class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='student_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=3, decimal_places=2, validators=[
                                                MinValueValidator(0), 
                                                MaxValueValidator(5)
                                              ])

    def __str__(self) -> str:
        return f"{self.student} enrolled in {self.course}"

class Tag(models.Model):
    '''
    Represents a tag for a module. e.g Software dev
    A skill that can be learned in a course or specific lesson 
    '''
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Module(models.Model):
    '''
    Represents a module in a course
    '''

    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    
    # Details
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='academy/courses/modules/', blank=True, null=True)
    
    # Datetime
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Grouping, categories
    tags = models.ManyToManyField(Tag, blank=True)

    REQUIRED_FIELDS = ['Course']

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Delete old thumbnail when making an update to the thumbnail 
        with contextlib.suppress(Exception):
            old = Module.objects.get(id=self.id)
            if old.thumbnail != self.thumbnail:
                old.thumbnail.delete(save=False)
        super().save(*args, **kwargs)  

class Lesson(models.Model):
    '''
    Represents a lesson in a module
    '''
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    
    # Details
    name = models.CharField(max_length=200)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module')
    
    # Resources
    video_url = models.URLField(blank=True, null=True)
    lesson_video = models.FileField(upload_to='academy/courses/lesson_materials/videos/', validators=[FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])], blank=True, null=True)
    lesson_documents = models.FileField(upload_to='academy/courses/lesson_materials/documents/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])], blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    # Datetime
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta: 
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_document_type(self):
        ext = str(self.lesson_documents).split(".")
        ext = ext[len(ext)-1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'    




    def __str__(self):
        return f"{self.name} in the {self.module.name} module"
          
class Quiz(models.Model):
    '''
    An assessment on a lesson 
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, default="Lesson Quiz")
    
    # Relationships
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_quizes")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
    TEXT_ANSWER = 'TA', 'Text Answer'
    URL_ANSWER = 'UA', 'URL Answer'

class QuizQuestion(models.Model):
    '''
    A data structure to represent an assessment question
    '''
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING, related_name="questions")
    #QUESTIONS
    question = models.CharField(max_length=1000)
    
    hint = models.TextField(null=True, blank=True)

    #ANSWERS
    correct_answer = models.CharField(max_length=1000,blank=True, null=True)
    options = models.JSONField(blank=True,  null=True)
    # ensure questionns, options and ansers match the question type in the serializer
    question_type = models.CharField(max_length=2, choices=QuestionType.choices)


    def __str__(self):
        return self.body
    
class Answer(models.Model):

     id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)

     # validate a amswer against its question in the serilizer
     # every time a new answer is created in the serializer validate if the answer is correct or not 
     # by fetching the corresponding question and checking if the answer is correct or not before saving or updating the answer
     answer = models.CharField(max_length=1000,blank=True, null=True)
     is_correct = models.BooleanField(default=False)
     question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, default='no_answer', related_name="answers")
     student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="student_answers")

    # to get student scores use aggregate function to get the sum of all correct answers for a student and divide by the total number of questions in a quiz


















# class QuizQuestionOption(models.Model):
#     '''
#     A data structure to represent an option on a multi choice question 
#     assessment type 
#     '''

#     id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
#     question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="options")
    
#     option_texts = models.CharField(max_length=200)
#     is_correct = models.BooleanField(default=False)
    
#     def __str__(self) -> str:
#         return f"Option: '{self.option_text}' on Question: {self.question}"




# class TagModule(models.Model):
#     # Represents the many-to-many relationship between tags and modules
#     id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     module = models.ForeignKey(Module, on_delete=models.CASCADE)

# # Reviews
# class InstructorReview(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4,)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="instructor_review_author")
#     instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
#     comment = models.TextField()
#     rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
#     # Datetime
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("author", "instructor")
#         ordering = ["updated_at"]
        
#     def __str__(self):
#         return f"Comment by {self.author.email} on {self.instructor.user.email}"

