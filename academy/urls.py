from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"courses", views.CourseViewSet, basename="course")
router.register(r"courses/tags", views.TagViewSet, basename="tags " )
# router.register(r"course/modules/",views.ModuleViewSet, basename="module")
# router.register(r"course/module/lessons",views.LessonViewSet, basename="lesson")
# router.register(r"course/module/lesson/quizzes",views.QuizViewSet, basename="quizzes")
# router.register(r"course/module/lesson/quiz/questions",views.QuizQuestionViewSet, basename="quiz")
router.register(r"course/module/lesson/quiz/question/answers",views.AnswerviewSet, basename="answer")
router.register(r"course/enrollment",views.EnrollmentViewSet, basename="enrollment")
router.register(r"studentprofile", views.StudentProfileViewSet, basename="studentprofile")
router.register(r"instructorsprofile", views.InstructorProfileViewSet, basename="instructorprofile")


urlpatterns = [
      path('', include(router.urls)),
      path("course/modules/",views.ModuleViewSet.as_view({"get":"by_course","post":"by_course"}), name="module-by-course"),
      path("course/module/lessons/",views.LessonViewSet.as_view({"get":"by-module","post":"by-module"}), name="lesson-by-module"),
      path("course/module/lesson/quizzes/",views.QuizViewSet.as_view({"get":"by_lesson","post":"by_lesson"}), name="quiz-by-lesson"),
      path("course/module/lesson/quiz/questions/",views.QuizQuestionViewSet.as_view({"get":"by_quiz","post":"by_quiz"}), name="quizquestion-by-quiz"),
      path("course/review/", views.CourseReviewViewSet.as_view({"get":"by_course","post":"by_course","delete":"by_course",}), name="coursereview-by-course"  ),
      path("course/search/", views.CourseSearchView.as_view(),name='search')
]

