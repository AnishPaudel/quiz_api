"""
Testing quiz models
"""

from django.test import TestCase
from quiz import models
from django.contrib.auth import get_user_model


def create_quiz(creator):

    quiz = models.Quiz.objects.get_or_create(
        discription="my first quiz", name="quiz2", creator=creator
    )  # noqa
    # quiz.save()
    return quiz[0]


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_create_quiz(self):
        """Test creating quiz"""
        user = create_user()
        quiz = models.Quiz.objects.create(
            discription="my first quiz", name="quiz1", creator=user
        )  # noqa
        self.assertEqual(str(quiz), quiz.name)

    def test_create_question(self):
        """Test creating quiz question"""
        user = create_user()
        question = models.QuizQuestion.objects.create(
            question="How are u ?", is_multi=True, creator=user
        )
        self.assertEqual(str(question), question.question)

    def test_create_question_option(self):
        """Test creating question-option"""
        answer = models.QuizAnswersOption.objects.create(
            answer="fine", is_answer=True
        )  # noqa

        self.assertEqual(str(answer), answer.answer)

    # def test_create_student_answer(self):
    #     """Test create student Answer model"""
    #     user = create_user()
    #     quiz = models.Quiz.objects.create(
    #         discription="my first quiz", name="quiz1", creator=user
    #     )  # noq

    #     question = models.QuizQuestion.objects.create(
    #         question="How are u ?", is_multi=True, creator=user
    #     )
    #     answer =
    #  models.QuizAnswersOption.objects.create(answer="fine", is_answer=True)
    #     question.options.add(answer)
    #     quiz.questions.add(question)

    #     std_student_option = models.QuizStudentAnswerOption.objects.create(
    #         std_answer=answer
    #     )

    #     std_anser_item =
    #  models.QuizStudentAnswerItem.objects.create(question=question)
    #     std_anser_item.options.add(std_student_option)

    #     std_anser = models.QuizStudentAnswer.objects.create(
    #         user=user,
    #         quiz=quiz,
    #     )
    #     std_anser.answers.add(std_anser_item)
    #     self.assertEqual(std_anser.user, user)
