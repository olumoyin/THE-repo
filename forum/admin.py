# from django.contrib import admin

# from .models import (
#     Topic,
#     Question,
#     Comment
# )

# @admin.register(Topic)
# class TopicAdmin(admin.ModelAdmin):
#     list_display = ["id",  "text", "author"]
#     list_filter = [ "author", "text" ]
#     search_fields = ["text", "author"]


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ["id",  "title", "author", "updated_at"]
#     list_filter = ["author", "updated_at"  ]
#     search_fields = ["title", "body", "author"]



# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ["id", "author", "answers_question", "updated_at"]
#     list_filter = ["author", "updated_at", "answers_question", "question"  ]
#     search_fields = [ "body", "author"]


