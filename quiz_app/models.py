# quiz_app/models.py

from django.db import models
import uuid
import json
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ])
    source_url = models.URLField(blank=True, null=True)  # optional source link

    def __str__(self):
        return self.question_text

class QuizSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_answered = models.IntegerField(default=0)
    total_correct = models.IntegerField(default=0)
    total_incorrect = models.IntegerField(default=0)
    seen_questions = models.TextField(default='[]')  # store seen Q IDs as JSON
    question_limit = models.IntegerField(default=10)  # how many questions user wants
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.session_id}"

    def get_seen_questions(self):
        return json.loads(self.seen_questions)

    def add_seen_question(self, q_id):
        seen = self.get_seen_questions()
        if q_id not in seen:
            seen.append(q_id)
            self.seen_questions = json.dumps(seen)
            self.save()

    def reset_seen_questions(self):
        self.seen_questions = '[]'
        self.save()
