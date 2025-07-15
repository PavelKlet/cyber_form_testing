from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from . import services
from .models import Test
from .serializers import (
    TestSerializer,
    SaveAnswerSerializer,
    FinishTestResultSerializer,
    TestSessionDetailSerializer, StartSessionResponseSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


class TestViewSet(ReadOnlyModelViewSet):
    queryset = Test.objects.prefetch_related('questions').all()
    serializer_class = TestSerializer


class StartTestSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: StartSessionResponseSerializer},
        description="Запускает сессию теста для пользователя"
    )
    def post(self, request, test_id):
        try:
            session = services.start_test_session(request.user, test_id)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "session_id": session.id,
            "test_id": session.test.id,
            "test_title": session.test.title
        }

        serializer = StartSessionResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SaveAnswerSerializer,
        responses={
            200: OpenApiResponse(
                response=None,
                description="Ответ сохранён",
                examples=[
                    OpenApiExample(
                        name="Успешный ответ",
                        value={"detail": "Ответ сохранён"},
                        response_only=True
                    )
                ]
            )
        },
        description="Сохраняет ответ пользователя на конкретный вопрос"
    )
    def post(self, request, session_id, question_id):
        serializer = SaveAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.save_user_answer(
            user=request.user,
            session_id=session_id,
            question_id=question_id,
            answers=serializer.validated_data['answer']
        )

        return Response({"detail": "Ответ сохранён"})


class FinishTestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        result_data = services.finish_test_session(request.user, session_id)
        serializer = FinishTestResultSerializer(result_data)
        return Response(serializer.data)


class TestSessionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        result = services.get_test_session_details(request.user, session_id)
        serializer = TestSessionDetailSerializer(result)
        return Response(serializer.data)

