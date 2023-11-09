# from django.contrib import admin

# from jobs.models import (
#     CompanyProfile,
#     CompanyReview,
#     HirerProfile,
#     Job,
#     Industry,
#     JobIndustry,
#     JobReview
# )


# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "location",  "salary", "status")
#     list_filter = ("location", "role_type")
#     search_fields = ( "title", "location", "salary",)


# @admin.register(Industry)
# class IndustryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']
#     list_filter = ['name']
#     search_fields = ['name']


# @admin.register(JobIndustry)
# class JobIndustryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'job', 'industry']
#     list_filter = ['job', 'industry']
#     search_fields = ['job']


# @admin.register(JobReview)
# class JobReviewAdmin(admin.ModelAdmin):
#     list_display = ['author', 'job', 'rating', 'comment', ]
#     list_filter = ['rating', 'job', 'created_at']
#     search_fields = ['author', 'job']

# @admin.register(HirerProfile)
# class HirerProfileAdmin(admin.ModelAdmin):
#     list_display  =  ["id", "user", "is_company", "company_id"]
#     list_filter   =  ["is_company"]
#     search_fields =  ["user"]

# @admin.register(CompanyProfile)
# class CompanyProfileAdmin(admin.ModelAdmin):
#     list_display  =  ["id", "name", "location", "founded", "revenue"]
#     list_filter   =  ["location"]
#     search_fields =  ["name", "location", "description"]

# @admin.register(CompanyReview)
# class CompanyReviewAdmin(admin.ModelAdmin):
#     list_display  =  ["id", "author", "company", "rating", "updated_at"]
#     list_filter   =  ["rating", "author", "company"]
#     search_fields =  ["comment", "author", "company"]

