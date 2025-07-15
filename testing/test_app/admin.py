from django.contrib import admin
from .models import Test, Question, TestSession, UserAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "test", "text", "question_type"]
    list_filter = ["test", "question_type"]
    search_fields = ["text"]


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "test", "is_finished", "score", "started_at", "finished_at"]
    list_filter = ["is_finished"]
    search_fields = ["user__username", "test__title"]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "session", "question"]
    search_fields = ["question__text"]
