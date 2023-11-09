import uuid
from django.db import models
from shortuuid.django_fields import ShortUUIDField

from users.models import BaseUserProfile, CompanyProfile


class ServiceLocation(models.Model):
    '''
    Represents a location where an internet service is offered
    '''
    SERVICE_TYPES = [
       ("wifi", 'wifi'),
       ("fibre", "fibre"),
       ("p2p/ptmp", "p2p/ptmp")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False)
    description = models.TextField()

    operator = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True, blank=True)

    # Location
    address = models.CharField(max_length=150, null=False, blank=False)
    latitude = models.DecimalField(max_digits=18, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)

    # Service
    service = models.CharField(max_length=10, choices=SERVICE_TYPES, null=False, blank=False)
    speed = models.IntegerField()

class SavedLocation(models.Model):
    '''
    Represents the raltionship between a user and the service locations they 
    have saved
    '''
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    saver = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name='saved_locations')
    locations = models.ManyToManyField(ServiceLocation)

    def locations_count(self):
        return self.locations.count()

class Regulation(models.Model):
    '''
    Represents the WISP regulation in region in a particular time
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.CharField(max_length=60)
    # Body in MDX
    body = models.TextField()
    year = models.DateField(null=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    


