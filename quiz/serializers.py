"""
Serializer for quiz API
"""


from rest_framework import serializers

from quiz.models import (
    Quiz,
    QuizQuestion,
    QuizAnswersOption,
)


#  Answer Options


class QuizAnswerOptionSerializer(serializers.ModelSerializer):
    """Serializer for quiz answer option"""

    class Meta:
        model = QuizAnswersOption
        fields = ["id", "answer", "is_answer"]
        read_only_fields = ["id"]


class QuizAnswerOptionStudentSerializer(QuizAnswerOptionSerializer):
    """Serializer for quiz answer option for students"""

    class Meta(QuizAnswerOptionSerializer.Meta):
        fields = ["id", "answer"]

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields


# Quiz Question


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Serializer for quiz questions"""

    options = QuizAnswerOptionSerializer(many=True, required=False)

    class Meta:
        model = QuizQuestion
        fields = ["id", "question", "is_multi", "options", "mark"]
        read_only_fields = ["id"]

    def _get_create_options(self, options, question):
        """Handle getting or creating questions as needed"""
        for option in options:
            option_obj, created = QuizAnswersOption.objects.get_or_create(
                **option
            )  # noqa
            question.options.add(option_obj)

    def create(self, validated_data):
        """Create a student answers."""
        options = validated_data.pop("options", [])

        question = QuizQuestion.objects.create(**validated_data)
        self._get_create_options(options, question=question)

        return question

    def update(self, instance, validated_data):
        """Update student answers"""
        options = validated_data.pop("options", None)
        if options is not None:
            instance.options.clear()
            self._get_create_options(options, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class QuizQuestionStudentSerializer(QuizQuestionSerializer):
    """Serializer for quiz questions"""

    options = QuizAnswerOptionSerializer(many=True, required=True)

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields


# Quiz


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quiz"""

    class Meta:
        model = Quiz
        fields = ["id", "name", "discription"]
        read_only_fields = ["id"]


class QuizDetailSerializer(QuizSerializer):
    """Serializer for quiz detail view"""

    questions = QuizQuestionSerializer(many=True, required=False)

    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ["questions"]

    def _get_create_options(self, options, question):
        """Handle getting or creating questions as needed"""
        for option in options:
            option_obj, created = QuizAnswersOption.objects.get_or_create(
                **option
            )  # noqa
            question.options.add(option_obj)

    def _get_create_questions(self, questions, quiz):
        """Handle getting or creating questions as needed"""
        auth_user = self.context["request"].user
        for question in questions:

            options = question.pop("options", [])

            question_obj, created = QuizQuestion.objects.get_or_create(
                creator=auth_user, **question
            )
            self._get_create_options(options=options, question=question_obj)
            quiz.questions.add(question_obj)

    def create(self, validated_data):
        """Create a quiz."""

        questions = validated_data.pop("questions", [])

        quiz = Quiz.objects.create(**validated_data)
        self._get_create_questions(questions, quiz=quiz)

        return quiz

    def update(self, instance, validated_data):
        """Update quiz"""
        questions = validated_data.pop("questions", None)
        if questions is not None:
            instance.questions.clear()
            self._get_create_questions(questions, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class QuizDetailStudentSerializer(QuizDetailSerializer):

    questions = QuizQuestionStudentSerializer(many=True, required=False)

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields
