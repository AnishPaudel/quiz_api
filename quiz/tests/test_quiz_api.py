"""
Test for quiz api
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from quiz.models import QuizAnswersOption, QuizQuestion, Quiz  # noqa
from quiz.serializers import QuizSerializer, QuizDetailSerializer

QUIZ_URL = reverse("quiz:quiz-list")


def detail_url(quiz_id):
    """Create and return a quiz detail URL"""
    return reverse("quiz:quiz-detail", args=[quiz_id])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_quiz(user, **params):
    """Create and return a sample reciepe"""
    defaults = {"name": "Sample Quiz title", "discription": "test description"}
    defaults.update(**params)
    quiz = Quiz.objects.create(creator=user, **defaults)
    return quiz


class PublicQuizzAPITests(TestCase):
    """Test unautenticate API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test auth is required to call api"""
        res = self.client.get(QUIZ_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQuizApiTestStaff(TestCase):
    """Test for autheticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com", password="test123", username="teststaff"
        )
        self.user.is_staff = True
        self.client.force_authenticate(self.user)

    def test_retrive_quizes(self):
        create_quiz(user=self.user)
        create_quiz(user=self.user)
        res = self.client.get(QUIZ_URL)
        quizes = Quiz.objects.all().order_by("-id")
        serializer = QuizSerializer(quizes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_quiz_list_limited_to_staff(self):
        """Test list of quizes is limited to authenicated user"""
        other_user = get_user_model().objects.create_user(
            email="other@example.com",
            password="password123",
            username="otherstaff",  # noqa
        )
        create_quiz(user=other_user)
        create_quiz(user=self.user)

        res = self.client.get(QUIZ_URL)

        reciepe = Quiz.objects.filter(creator=self.user)
        serializer = QuizSerializer(reciepe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_quiz_detail(self):
        """Test get quiz detail"""
        quiz = create_quiz(user=self.user)

        url = detail_url(quiz_id=quiz.id)
        res = self.client.get(url)

        serializer = QuizDetailSerializer(quiz)
        self.assertEqual(res.data, serializer.data)

    def test_create_quiz(self):
        """Test creating quiz."""
        payload = {"name": "Quiz2", "discription": "Best of luck"}
        res = self.client.post(QUIZ_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        quiz = Quiz.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(quiz, k), v)
        self.assertEqual(quiz.creator, self.user)

    def test_update_user_returns_error(self):
        """Test changingng the quiz creator results in an error."""
        new_user = create_user(
            email="user2@exampl.com", password="test123", username="test12"
        )
        quiz = create_quiz(user=self.user)
        payload = {"user": new_user.id}
        url = detail_url(quiz_id=quiz.id)

        self.client.patch(url, payload)
        quiz.refresh_from_db()
        self.assertEqual(quiz.creator, self.user)

    def test_create_quiz_with_question_answers(self):
        """Test creating quiz with question and ansers"""
        payload = {
            "name": "Quiz3",
            "questions": [
                {
                    "question": "How are you",
                    "is_multi": True,
                    "options": [{"answer": "I am good", "is_answer": True}],
                },
                {
                    "question": "How are you now",
                    "is_multi": False,
                    "options": [
                        {"answer": "I am good may be", "is_answer": True}
                    ],  # noqa
                },
            ],
        }
        res = self.client.post(QUIZ_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        quizs = Quiz.objects.filter(creator=self.user)
        self.assertEqual(quizs.count(), 1)
        quiz = quizs[0]
        self.assertEqual(quiz.questions.count(), 2)
        for q in payload["questions"]:
            exist = quiz.questions.filter(
                question=q["question"], creator=self.user
            ).exists()  # noqa
            self.assertTrue(exist)  # todo
            # print(quiz.questions.filter(
            #     question=q["question"], user=self.user
            # ))

    def test_create_quiz_with_existing_questions_and_answer(self):
        """Test creating quiz with existing question and answer."""
        answer = QuizAnswersOption.objects.create(
            answer="I am good", is_answer=True
        )  # noqa
        question = QuizQuestion.objects.create(
            question="How are you??", is_multi=True, creator=self.user
        )  # noqa
        question.options.add(answer)
        payload = {
            "name": "Quiz4",
            "questions": [
                {
                    "question": "How are you??",
                    "is_multi": True,
                    "options": [{"answer": "I am good", "is_answer": True}],
                },
                {
                    "question": "How are you now",
                    "is_multi": False,
                    "options": [
                        {"answer": "I am good may be", "is_answer": True}
                    ],  # noqa
                },
            ],
        }
        res = self.client.post(QUIZ_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        quizes = Quiz.objects.filter(creator=self.user)
        self.assertEqual(quizes.count(), 1)
        quiz = quizes[0]
        self.assertEqual(quiz.questions.count(), 2)
        self.assertIn(question, quiz.questions.all())
        for q in payload["questions"]:
            exist = quiz.questions.filter(
                question=q["question"], creator=self.user
            ).exists()  # noqa
            self.assertTrue(exist)

    def test_create_question_on_update(self):
        """Test create tag on update update of reciepe"""
        quid = create_quiz(user=self.user)
        payload = {
            "questions": [
                {
                    "question": "How are you??",
                    "is_multi": True,
                    "options": [{"answer": "I am good", "is_answer": True}],
                }
            ],
        }
        url = detail_url(quiz_id=quid.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        question = QuizQuestion.objects.filter(question="How are you??")
        self.assertEqual(question.count(), 1)
        self.assertIn(question[0], quid.questions.all())

    def test_update_quiz_assign_questions(self):
        """Test assigning  an existing tag when updating a reciepe"""
        answer = QuizAnswersOption.objects.create(
            answer="I am good ", is_answer=True
        )  # noqa
        question_old = QuizQuestion.objects.create(
            question="How are you1 ??", is_multi=True, creator=self.user
        )
        question_old.options.add(answer)
        quiz = create_quiz(user=self.user)
        quiz.questions.add(question_old)

        question_new = QuizQuestion.objects.create(
            question="How are you??", is_multi=True, creator=self.user
        )
        question_new.options.add(answer)

        payload = {
            "questions": [
                {
                    "question": "How are you??",
                    "is_multi": True,
                    "options": [{"answer": "I am good", "is_answer": True}],
                }
            ]
        }
        url = detail_url(quiz_id=quiz.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(question_new, quiz.questions.all())
        self.assertNotIn(question_old, quiz.questions.all())

    def test_clear_questions_tags(self):
        """Test clearing aceipes tags."""
        answer = QuizAnswersOption.objects.create(
            answer="I am good", is_answer=True
        )  # noqa
        question = QuizQuestion.objects.create(
            question="How are you??", is_multi=True, creator=self.user
        )  # noqa
        question.options.add(answer)
        quiz = create_quiz(user=self.user)
        quiz.questions.add(question)

        payload = {"questions": []}
        url = detail_url(quiz_id=quiz.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(quiz.questions.count(), 0)


class PrivateQuizApiTestStudent(TestCase):
    """Test for autheticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com", password="test123", username="teststaff"
        )
        self.user.is_staff = False
        self.client.force_authenticate(self.user)

    def test_student_quiz_readonly(self):
        """testing student quiz read only on update quiz"""
        question_new = QuizQuestion.objects.create(
            question="How are you??", is_multi=True, creator=self.user
        )
        quiz = create_quiz(user=self.user)
        quiz.questions.add(question_new)

        payload = {
            "questions": [
                {
                    "question": "How are you??",
                    "is_multi": True,
                    "options": [{"answer": "I am good", "is_answer": True}],
                }
            ]
        }
        url = detail_url(quiz_id=quiz.id)
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
