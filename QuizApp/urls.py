from django.urls import path
from QuizApp import views

app_name = "QuizApp"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:student_id>/', views.student_results, name='student_results'),
    path('avarage-quizzes-chart/<quiz_id>/', views.avarage_quizzes_chart, name='avarage-quizzes-chart'),
    path('quizzes-chart/<int:std_id>/<quiz_id>/', views.quizzes_chart, name='quizzes-chart'),
]