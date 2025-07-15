from rest_framework import serializers
from .models import Test, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'choices', 'correct_answers']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'questions']

class SaveAnswerSerializer(serializers.Serializer):
    answer = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        help_text="Список выбранных ответов"
    )

class StartSessionResponseSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    test_id = serializers.IntegerField()
    test_title = serializers.CharField()

class FinishTestResultSerializer(serializers.Serializer):
    score = serializers.FloatField()
    total = serializers.IntegerField()
    correct = serializers.IntegerField()

class QuestionWithAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    question_type = serializers.CharField()
    choices = serializers.ListField(child=serializers.CharField())
    user_answer = serializers.ListField(child=serializers.CharField())

class TestSessionDetailSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    test_title = serializers.CharField()
    is_finished = serializers.BooleanField()
    score = serializers.FloatField(allow_null=True)
    questions = QuestionWithAnswerSerializer(many=True)
