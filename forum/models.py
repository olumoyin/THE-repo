from django.db import models
import uuid
from users.models import BaseUserProfile




class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="topics")
    text = models.CharField(max_length=60, unique=True)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    author = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name="asked_questions")
    subjects = models.ManyToManyField(Subject)

    # Body
    title = models.CharField(max_length=180) 
    body = models.TextField()
    
    # Metrics
    voters = models.ManyToManyField(BaseUserProfile, blank=True, related_name="voted_questions")
    liked_by = models.ManyToManyField(BaseUserProfile, blank=True, related_name="liked_questions")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    '''
    A comment under/relating to a question that can be marked as an answer by the 
    question's author and voted or liked by other authenticated users
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships
    author = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name="comments")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    
    body = models.TextField()
    
    # Metrics
    answers_question = models.BooleanField(default=False)
    voters = models.ManyToManyField(BaseUserProfile, blank=True, related_name="voted_comments")
    liked_by = models.ManyToManyField(BaseUserProfile, blank=True, related_name="liked_comments")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


