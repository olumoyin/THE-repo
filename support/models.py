from django.db import models
import uuid
from users.models import BaseUserProfile


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(BaseUserProfile, on_delete=models.DO_NOTHING, related_name='complaints')
    
    # Body
    title = models.CharField(max_length=200)
    message = models.TextField()

    # Metrics
    is_resolved = models.BooleanField(default=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


