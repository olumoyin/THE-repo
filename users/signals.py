from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
# from wta_api_build import settings

from users.models import BaseUserProfile, CompanyProfile, HirerProfile 
from academy.models import StudentProfile, InstructorProfile


#settings.AUTH_USER_MODEL

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    '''
    Creates a company profile for every user created, if said user is_organisation.
    If not, creates a BaseUserProfile for it
    '''
    if created:
        if instance.is_organisation:
            try:
                company_profile = CompanyProfile.objects.create(organisation=instance)
                if instance.is_hirer:
                    HirerProfile.objects.create(company_profile=company_profile, is_company=True)
                    print("Hirer Profile created")
                return 
            except:
                print("Company profile wasn't created")
                return None
        
        try:
            base_profile = BaseUserProfile.objects.create(user=instance)
        except:
            print("Base user profile wasn't created")
            return None
        if instance.is_instructor:
            InstructorProfile.objects.create(user_profile=base_profile)
            print("Instructor Profile created")
        if instance.is_student:
            StudentProfile.objects.create(user_profile=base_profile)
            print("Student Profile created")
        if instance.is_hirer:
            HirerProfile.objects.create(user_profile=base_profile)
            print("Hirer Profile created")


# @receiver(post_save, sender=get_user_model())
# def create_user_profile(sender, instance, **kwargs):

#     if instance.is_student:

