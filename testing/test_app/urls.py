from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StartTestSessionAPIView,
    TestSessionDetailAPIView,
    FinishTestAPIView,
    SaveAnswerAPIView,
    TestViewSet
)

router = DefaultRouter()
router.register(r'tests', TestViewSet, basename='test')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/tests/<int:session_id>/finish/', FinishTestAPIView.as_view(), name='test-finish'),
    path('api/tests/<int:session_id>/questions/<int:question_id>/answer/', SaveAnswerAPIView.as_view(), name='save-answer'),
    path('api/tests/<test_id>/start/', StartTestSessionAPIView.as_view(), name='start-test'),
    path('api/sessions/<session_id>/', TestSessionDetailAPIView.as_view(), name='test-session'),
]
