from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Test, TestSession, Question, UserAnswer


def start_test_session(user, test_id):
    test = get_object_or_404(Test, id=test_id)

    session, created = TestSession.objects.get_or_create(
        user=user,
        test=test,
        defaults={'is_finished': False}
    )

    if not created and session.is_finished:
        raise ValueError("Тест уже завершён")

    return session


def save_user_answer(user, session_id, question_id, answers):
    session = get_object_or_404(TestSession, id=session_id, user=user, is_finished=False)
    question = get_object_or_404(Question, id=question_id, test=session.test)

    UserAnswer.objects.update_or_create(
        session=session,
        question=question,
        defaults={'answer': answers}
    )
    return session, question


def finish_test_session(user, session_id):
    session = get_object_or_404(TestSession, id=session_id, user=user, is_finished=False)
    answers = session.answers.select_related('question')

    correct_count = 0
    total_questions = session.test.questions.count()

    for answer in answers:
        correct_answers = set(answer.question.correct_answers)
        user_answers = set(answer.answer)
        if correct_answers == user_answers:
            correct_count += 1

    score = (correct_count / total_questions * 100) if total_questions else 0

    session.score = score
    session.is_finished = True
    session.finished_at = timezone.now()
    session.save()

    return {
        "score": score,
        "total": total_questions,
        "correct": correct_count
    }


def get_test_session_details(user, session_id):
    session = get_object_or_404(TestSession, id=session_id, user=user)
    questions = session.test.questions.all()
    user_answers = {ua.question_id: ua.answer for ua in session.answers.all()}

    questions_data = [
        {
            "id": q.id,
            "text": q.text,
            "question_type": q.question_type,
            "choices": q.choices,
            "user_answer": user_answers.get(q.id, []),
        }
        for q in questions
    ]

    return {
        "test_id": session.test.id,
        "test_title": session.test.title,
        "is_finished": session.is_finished,
        "score": session.score,
        "questions": questions_data,
    }
