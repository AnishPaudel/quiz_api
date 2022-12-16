"""
Serializers for student answers api
"""

from rest_framework import serializers
from answer.models import (
    QuizStudentAnswerItem,
    QuizStudentAnswer,
    QuizStudentAnswerOption,
)


class QuizStdAnserOptionSerializer(serializers.ModelSerializer):
    """Serialiser for answer option"""

    class Meta:
        model = QuizStudentAnswerOption
        fields = ["id", "std_answer"]
        read_only_fields = ["id"]

    # def create(self, validated_data):
    #     option_id = validated_data.pop("std_answer")
    #     option = QuizAnswersOption.objects.get(id=option_id)

    #     std_ans_option = QuizStudentAnswerOption.create(
    #         std_answer=option, **validated_data
    #     )

    #     return std_ans_option


class QuizStudentAnswerItemSerializer(serializers.ModelSerializer):

    options = QuizStdAnserOptionSerializer(many=True, required=True)

    class Meta:
        model = QuizStudentAnswerItem
        fields = ["id", "question", "options"]
        read_only_fields = ["id"]

    # def create(self, validated_data):
    #     print("Creating answer itme")
    #     questionId_id = validated_data.pop("quiz")
    #     question = QuizQuestion.objects.get(id=questionId_id)
    #     quiz_ans = QuizStudentAnswerItem.objects.create(
    #         question=question, **validated_data
    #     )  # noqa

    #     return quiz_ans


class QuizStudentAnswerSerializer(serializers.ModelSerializer):
    """Serializer for student Answer"""

    # quiz = serializers.IntegerField()
    answers = QuizStudentAnswerItemSerializer(many=True, required=True)

    class Meta:
        model = QuizStudentAnswer
        fields = ["id", "quiz", "answers"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "answers": {"required": "True"},
            "quiz": {"required": "True"},
        }

    def _get_create_options(self, options, anserItem):
        """Handle getting or creating options as needed"""
        for option in options:

            option_obj = QuizStudentAnswerOption.objects.create(**option)  # noqa
            anserItem.options.add(option_obj)

    def _get_create_answe_item(self, ans_items, quiz_answer):
        """Handle getting or creating answer item as needed"""
        for ans_item in ans_items:
            options = ans_item.pop("options", [])
            question_obj = QuizStudentAnswerItem.objects.create(**ans_item)
            self._get_create_options(options=options, anserItem=question_obj)
            quiz_answer.answers.add(question_obj)

    def create(self, validated_data):

        # print("Creating anseer", validated_data)
        quiz = validated_data.pop("quiz")
        answers = validated_data.pop("answers", [])
        quiz_ans = QuizStudentAnswer.objects.create(quiz=quiz, **validated_data)  # noqa
        self._get_create_answe_item(ans_items=answers, quiz_answer=quiz_ans)
        # print("Created", quiz_ans.answers.all())
        return quiz_ans

    def update(self, instance, validated_data):
        # print("updating", instance)
        answers = validated_data.pop("answers", None)
        if answers is not None:
            print(instance)
            instance.answers.clear()
            self._get_create_answe_item(ans_items=answers, quiz_answer=instance)  # noqa

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate(self, attrs):
        # do single choice option only one validatio
        # also the values must exist in question

        data = super().validate(attrs)
        # print("data after validation", data)
        quiz = data["quiz"]
        answers = data["answers"]

        for answer in answers:
            question_ans = answer["question"]
            # print(quiz.questions.all())
            if question_ans not in quiz.questions.all():
                raise serializers.ValidationError(
                    "Question doesnt belong to quiz"
                )  # noqa
            options = answer["options"]
            for option in options:

                option_ans = option["std_answer"]
                if option_ans not in question_ans.options.all():
                    raise serializers.ValidationError(
                        "Option doesnt belong to question"
                    )

        return data
