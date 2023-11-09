from django.contrib import admin

from .models import (
    BaseUserProfile,
    CompanyProfile,
    HirerProfile,
    InstructorProfile,
    StudentProfile,
    User,
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "is_organisation")
    list_filter = ( "is_instructor", "is_student", "is_hirer", "is_staff", "is_superuser")
    search_fields = ( "email", "username", "first_name", "last_name",)

@admin.register(BaseUserProfile)
class BaseUserProfileAdmin(admin.ModelAdmin):
    list_display  =  ["id", "first_name", "last_name",  "user", "gender"]
    list_filter   =  ["gender"]
    search_fields =  ["first_name", "last_name", "user"]

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display  =  ["id", "user_profile", "bio"]


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display  =  ["id", "user_profile", "bio"]

@admin.register(HirerProfile)
class HirerProfileAdmin(admin.ModelAdmin):
    list_display  =  ["id", "user_profile", "company_profile", "is_company", "bio"]
    list_filter   =  ["is_company"]
    search_fields =  ["user_profile", "company_profile", "bio"]

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display  =  ["id", "name", "country", "revenue", "founded"]
    list_filter   =  ["country", "founded"]
    search_fields =  ["name", "desciption"]