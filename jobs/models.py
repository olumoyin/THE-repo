from django.db import models
import uuid
from users.models import BaseUserProfile, HirerProfile
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import MinValueValidator, MaxValueValidator

from wta_api_build import settings

class Industry(models.Model):
    '''
    # Represents an industry type e.g Networking
    A field that a company operates in 
    '''
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=255)


class Job(models.Model):
    '''
    A job listing with all its details 
    '''
    CURRENCIES = (
        ("NGN", "Naira"),
        ("USD", "US Dollar"),
        ("GBP", "GB Pounds"),
    )
    STATUS = (
        ("open", "Open"),
        ("filled", "Filled"),  
        ("unavailable", "Unavailable"),
    )
    ROLE_TYPE = (
        ("remote", "Remote"),
        ("permanent", "Permanent"),  
        ("contract", "Contract"),
        ("hybrid", "Hybrid"),
        ("full-time", "Full time"),  
        ("internship", "Internship"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False)
    listed_by = models.ForeignKey(HirerProfile,  on_delete=models.CASCADE, related_name='listed_jobs')
    
    # Job description
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField()
    location = models.CharField(max_length=250, null=False, blank=False)
    salary = models.DecimalField(max_digits=3, decimal_places=2, default=99999)
    salary_currency = models.CharField(max_length=10, choices=CURRENCIES, default="NGN")
    status = models.CharField(max_length=15, choices=STATUS, default="Open")
    role_type = models.CharField(max_length=10, choices=ROLE_TYPE, default="Permanent")

    # Metrics
    liked_by = models.ManyToManyField(BaseUserProfile, blank=True)
    industries = models.ManyToManyField(Industry, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} is {self.status}"



    def __str__(self):
        return self.name

    




# class JobIndustry(models.Model):
#     # Represents the many-to-many relationship between Jobs and Industries
#     id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE)
#     industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.industry.name} on {self.job.name}"
    
# # Reviews
# class CompanyReview(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_review_author")
#     company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
#     comment = models.TextField()
#     rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
#     # Datetime
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("author", "company")
#         ordering = ["updated_at"]
        
#     def __str__(self):
#         return f"Comment by {self.author.email} on {self.company.name}"    

# class JobReview(models.Model):
#     id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    
#     # Relationships
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_job_reviews")
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="reviews")
    
#     # Body
#     comment = models.TextField()
#     rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
#     # Datetime
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         unique_together = ("author", "job")
#         ordering = ["updated_at"]
        
#     def __str__(self):
#         return f"Comment by {self.author.email} on {self.job.name}" 
    

