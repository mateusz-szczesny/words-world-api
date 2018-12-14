from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Language, Question, Answer, Achievement


class AchievementBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'condition', 'font_awesome_icon')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    achievements = AchievementBaseSerializer(many=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'groups', 'achievements')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class QuestionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'context', 'external_source', 'language', 'question_type', 'get_gap_markdown')


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionBaseSerializer(many=False)

    class Meta:
        model = Answer
        fields = ('id', 'context', 'is_correct', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    language = LanguageSerializer(many=False)

    class Meta:
        model = Question
        fields = ('id', 'context', 'external_source', 'language', 'question_type', 'answers', 'get_gap_markdown')
        depth = 2
