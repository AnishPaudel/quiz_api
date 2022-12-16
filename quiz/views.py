"""
Views for the quiz api

"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from quiz.models import Quiz
from quiz import serializers


class QuizViewSet(viewsets.ModelViewSet):
    """View for managing quiz object"""

    serializer_class = serializers.QuizDetailStudentSerializer
    queryset = Quiz.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        is_staff = self.request.user.is_staff
        if is_staff:
            return self.queryset.filter(creator=self.request.user).order_by(
                "-id"
            )  # noqa
        return self.queryset

    def get_serializer_class(self):
        """Return the serializer class for request"""
        is_staff = self.request.user.is_staff

        if self.action == "list":
            return serializers.QuizSerializer
        elif is_staff:  # for staff with answer
            return serializers.QuizDetailSerializer
        else:  # with no answer
            return serializers.QuizDetailStudentSerializer

    def perform_create(self, serializer):
        "create new quiz"
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        is_staff = self.request.user.is_staff
        if is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)  # noqa

    def update(self, request, *args, **kwargs):
        is_staff = self.request.user.is_staff
        if is_staff:
            return super().update(request, *args, **kwargs)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)  # noqa

    # def _calculate_student_marks(student_answer, quiz: Quiz):
    #     answer_models = []
    #     for answer in student_answer:
    #         answer_models.append(
    #             StudentAnswerJsonModelItem(
    #                 question_id=answer["question_id"],
    #  answer_ids=answer["answer_ids"]
    #             )
    #         )

    #     total = 0
    #     correct_questions = []
    #     for ans in answer_models:
    #         question = quiz.questions.get(id=ans.question_id)
    #         if question is not None:
    #             is_sucess = True
    #             if question.ismulti:
    #                 for a in question.options:
    #                     if a.id not in ans.answer_ids:
    #                         is_sucess = False
    #             else:
    #                 if len(ans.answer_ids) == 1:
    #                     answer = question.options.get(id=ans.answer_ids[0])
    #                 else:
    #                     return "Mulitple ansers given to single
    #  answer question"

    #             if is_sucess:
    #                 total = total + question.mark
    #                 correct_questions.append(question)

    #         else:
    #             return "Question id not found"

    #     return total
