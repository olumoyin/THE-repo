from datetime import date
from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from users.manager import UserManager
from wta_api_build import settings




# User Auth Model
class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Details
    email = models.EmailField(unique=True, null=False, blank=False)
    
    username = models.CharField(max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    # Roles
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_hirer = models.BooleanField(default=False)
    is_job_hunting = models.BooleanField(default=False)

    # User Type
    is_organisation = models.BooleanField(default=False)
    is_wisp_operator = models.BooleanField(default=False)


    # Verification
    is_verified = models.BooleanField(default=False)
    

    # DateTime
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_verified = True 
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email




# Base Profile and Profiles 
class BaseUserProfile(models.Model):
    '''
    A profile to contain a user's personal info
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Further info
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_fullname()
        return self.user.email

    
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        '''
        Sets user profile ID to the same as the user ID
        '''
        self.id = self.user.id
        super().save(*args, **kwargs)

class CompanyProfile(models.Model):
    '''
    A profile that contains an organisation's information
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_profile" )
    
    # Details
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    # location = models.CharField(max_length=360, null=True, blank=True)
    contact = PhoneNumberField(blank=True, null=True)
    revenue = models.IntegerField(null=True, blank=True)
    founded = models.DateField(default=date(2000, 10, 23), null=True, blank=True)

    # HQ/Branch Details
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    # Brand identity
    brand_logo = models.ImageField(upload_to="users/companies/brand_logos", null=True, blank=True)
    cover_image = models.ImageField(upload_to="users/companies/cover_images", null=True, blank=True)
    culture = models.TextField(null=True, blank=True)

    # Socials
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    x = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)

    
    # DateTime
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name:
            return self.name
        return self.organisation.email

    def save(self, *args, **kwargs):
        '''
        Sets user companyprofile's ID to the same as it's organisation ID
        '''
        self.id = self.organisation.id
        super().save(*args, **kwargs)

class InstructorProfile(models.Model):
    '''
    Represents a [Instructor] dashboard that contains further information of a 
    user who is registered as a instructor. 
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name='instructor_profile')
    instructor_pfp = models.ImageField(upload_to='users/profile_pictures/instructors/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Vanity Metrics
    # total_students = models.PositiveIntegerField(default=0, null=True, blank=True)
    rating  = models.PositiveIntegerField(default=0, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True) 

    class Meta:
        verbose_name_plural = 'Instructor Profiles'

    def instructor_fullname(self):
        return f"{self.user_profile.get_fullname()}'s Instructor's profile"
    
    def save(self, *args, **kwargs):
        '''
        Sets instructor ID to the same as the user ID
        '''
        self.id = self.user_profile.id
        super().save(*args, **kwargs)

class StudentProfile(models.Model):
    '''
    Represents a user's student dashboard: The relationship between 
    a user and the courses they have enrolled in
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f"{self.user_profile.get_fullname()}'s student profile"
    
    def student_fullname(self):
        return self.user_profile.get_fullname()
    
    def save(self, *args, **kwargs):
        '''
        Sets student ID to the same as the user ID
        '''
        self.id = self.user_profile.id
        super().save(*args, **kwargs)

class HirerProfile(models.Model):
    '''
    Represents a user or organsation's hirer dashboard: The relationship between 
    a user and the courses they have enrolled in
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hirer_pfp = models.ImageField(upload_to='users/profile_pictures/hirers/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # User
    user_profile = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="hirer_profile")
    company_profile = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,  null=True, blank=True, related_name="company_hirer_profile")

    is_company = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Hirer Profiles'

    def __str__(self):
        if self.is_company:
            return f"{self.company_profile.name}'s hirer profile"
        return f"{self.user_profile.get_fullname()}'s hirer profile"

    
    def save(self, *args, **kwargs):
        '''
        Sets hirer ID to the same as the user  or company's ID
        '''
        if self.is_company:
            id  = self.company_profile.id
        else:
            id = self.user_profile.id
        
        self.id = id
        super().save(*args, **kwargs)





