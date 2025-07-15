import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from test_app.models import Test, Question

class Command(BaseCommand):
    help = 'Импортирует тесты из CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_path = options['csv_file']

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            grouped = {}

            for row in reader:
                title = row['test_title']
                grouped.setdefault(title, []).append(row)

            for title, questions in grouped.items():
                with transaction.atomic():
                    test, _ = Test.objects.get_or_create(title=title)

                    test.questions.all().delete()

                    questions_objs = []

                    for q in questions:
                        questions_objs.append(
                            Question(
                                test=test,
                                text=q['question_text'],
                                question_type=q['question_type'],
                                choices=q['choices'].split(','),
                                correct_answers=q['correct_answers'].split(','),
                            )
                        )
                    Question.objects.bulk_create(questions_objs)
                    self.stdout.write(self.style.SUCCESS(f"Импортирован тест: {title}"))
