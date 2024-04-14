from django.contrib import admin
from .models import Course,Quizzes,QuizQuestions
from .models import QuizAttendance,QuizChoices
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Quizzes)
admin.site.register(QuizAttendance)
admin.site.register(QuizChoices)
admin.site.register(QuizQuestions)