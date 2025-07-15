from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

class Test(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    SINGLE = "single"
    MULTIPLE = "multiple"
    TEXT = "text"

    QUESTION_TYPES = [
        (SINGLE, "Один вариант"),
        (MULTIPLE, "Несколько вариантов"),
        (TEXT, "Текстовый ответ"),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    choices = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    correct_answers = ArrayField(models.CharField(max_length=255), blank=True, default=list)

    def __str__(self):
        return self.text


class TestSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "test")

    def __str__(self):
        return f"{self.user} - {self.test}"


class UserAnswer(models.Model):
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = ArrayField(models.CharField(max_length=255))

    class Meta:
        unique_together = ("session", "question")

