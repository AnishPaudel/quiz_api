"""
apis for managing student answer
"""

from rest_framework import viewsets, status, mixins


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from answer import serializers
from answer.models import QuizStudentAnswer
from user_stat.models import UserStat


class StudentQuizAnswersViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """View for managing student answers"""

    serializer_class = serializers.QuizStudentAnswerSerializer
    queryset = QuizStudentAnswer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # student can only view therier own answers but staff can view all student
    # answers
    def get_queryset(self):
        is_staff = self.request.user.is_staff
        if is_staff:
            return self.queryset
        return self.queryset.filter(creator=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        "create new student answer"
        serializer.save(user=self.request.user)

    def _calculate_marks_and_return_response(self, res):
        if (
            res.status_code == status.HTTP_201_CREATED
            or res.status_code == status.HTTP_200_OK
        ):
            std_ans_id = res.data["id"]
            student_answer = QuizStudentAnswer.objects.get(id=std_ans_id)
            total = 0
            correct_answers = 0
            incorrect_answers = 0
            for item in student_answer.answers.all():
                # print(item.question.is_multi)
                question = item.question
                sucess = True
                if item.options.count() > 0:  # user has marks
                    if question.is_multi:
                        for option in question.options.all():
                            if option.is_answer:
                                if not item.options.filter(
                                    std_answer=option
                                ).exists():  # noqa
                                    sucess = False
                            else:
                                if item.options.filter(
                                    std_answer=option
                                ).exists():  # noqa
                                    sucess = False
                    else:
                        sucess = list(item.options.all())[
                            0
                        ].std_answer.is_answer  # noqa

                    if not sucess:  # gave anser but incorrect
                        incorrect_answers = incorrect_answers + 1

                else:
                    sucess = False
                if sucess:
                    total = total + question.mark
                    correct_answers = correct_answers + 1

            # print("Totalmark", total)
            self._update_user_stat(
                total,
                correct_answers=correct_answers,
                incorrect_answers=incorrect_answers,
            )

            # print(student_answer)
            res.data = {
                "marks_obtained": total,
                "correct_answers": correct_answers,
                "incorrect_answers": incorrect_answers,
                "answers_given": res.data,
            }  # noqa

        return res

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)

        return self._calculate_marks_and_return_response(res)

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        # print("upres", res)
        return self._calculate_marks_and_return_response(res)

    def _update_user_stat(
        self, marksObtained: float, correct_answers: int, incorrect_answers: int  # noqa
    ):
        user = self.request.user
        count = QuizStudentAnswer.objects.filter(user=user).count()
        user_stat, created = UserStat.objects.get_or_create(user=user)
        print("count--", count)

        user_stat.correct = user_stat.correct + correct_answers
        user_stat.total_score = user_stat.total_score + marksObtained
        user_stat.over_all_score = user_stat.total_score / count
        user_stat.incorrect = user_stat.incorrect + incorrect_answers
        user_stat.save()

    # @action(methods=["POST"], detail=True, url_path="std-ans")
    # def student_answers(self, request, pk=None):
    #     "handle student answer request"
    #     quiz = self.get_object()
    #     print(request.data)
    #     serializer = self.get_serializer(quiz, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save(user=self.request.user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     print(serializer.errors)
    #     return Response(serializer.errors,
    #  status=status.HTTP_400_BAD_REQUEST)
    # add code to calculate and save
