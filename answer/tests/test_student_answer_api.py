"""
Test for quiz answer  api
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from quiz.models import QuizAnswersOption, QuizQuestion, Quiz  # noqa


STUDENTS_ANSWERS_URL = reverse("answer:quizstudentanswer-list")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_quiz(user, **params):
    """Create and return a sample reciepe"""
    defaults = {"name": "Sample Quiz title", "discription": "test description"}
    defaults.update(**params)
    quize = Quiz.objects.create(creator=user, **defaults)

    return quize


class PrivateQuizAnswersApiTestStudent(TestCase):
    """Test for autheticated answer quiz API requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com", password="test123", username="teststaff"
        )
        self.user.is_staff = False
        self.client.force_authenticate(self.user)
        self.quiz = create_quiz(self.user)
        self.question = QuizQuestion.objects.create(
            question="How are u ?", is_multi=True, creator=self.user
        )
        self.answer1 = QuizAnswersOption.objects.create(
            answer="fine", is_answer=True
        )  # noqa
        self.answer2 = QuizAnswersOption.objects.create(answer="not fine")  # noqa
        self.question.options.add(self.answer1)
        self.question.options.add(self.answer2)
        self.quiz.questions.add(self.question)

    def test_create_quiz_answer(self):
        "Create Quiz student Ansers from api"

        payload = {
            "quiz": self.quiz.id,
            "answers": [
                {
                    "question": self.question.id,
                    "options": [{"std_answer": self.answer1.id}],
                }
            ],
        }

        res = self.client.post(STUDENTS_ANSWERS_URL, payload, format="json")
        # print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_data(self):
        """Test creating invalid data"""
        quiz = create_quiz(self.user)
        question = QuizQuestion.objects.create(
            question="How are u ?", is_multi=True, creator=self.user
        )
        answer = QuizAnswersOption.objects.create(answer="fine", is_answer=True)  # noqa
        question.options.add(answer)
        quiz.questions.add(question)
        # anser doesn belong to question
        answer2 = QuizAnswersOption.objects.create(
            answer="finedd", is_answer=True
        )  # noqa
        payload = {
            "quiz": quiz.id,
            "answers": [
                {
                    "question": question.id,
                    "options": [{"std_answer": answer2.id}],
                }  # noqa
            ],
        }

        res = self.client.post(STUDENTS_ANSWERS_URL, payload, format="json")

        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_marks_on_submission(self):
        """test returns marks on submissin"""
        payload = {
            "quiz": self.quiz.id,
            "answers": [
                {
                    "question": self.question.id,
                    "options": [{"std_answer": self.answer1.id}],
                }
            ],
        }

        res = self.client.post(STUDENTS_ANSWERS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["marks_obtained"], 1.0)

    # def test_get_student_answer(self):
    #     payload = {
    #         "quiz": self.quiz.id,
    #         "answers": [
    #             {
    #                 "question": self.question.id,
    #                 "options": [{"std_answer": self.answer1.id}],
    #             }
    #         ],
    #     }

    #     res = self.client.post(STUDENTS_ANSWERS_URL, payload, format="json")
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data["marks_obtained"], 1.0)
