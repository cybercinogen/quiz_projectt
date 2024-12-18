# quiz_app/admin.py
from django.contrib import admin
from .models import Question, QuizSession

admin.site.register(Question)
admin.site.register(QuizSession)
