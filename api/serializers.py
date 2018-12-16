from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Language, Question, Answer, Achievement, Score, Challenge, GivenAnswer, Round


class AchievementBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'condition', 'font_awesome_icon')


class QuestionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'context', 'external_source',
                  'language', 'question_type', 'get_gap_markdown',
                  'difficulty')


class AnswerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'context', 'is_correct')


class UserBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserAchievementsSerializer(serializers.HyperlinkedModelSerializer):
    achievements = AchievementBaseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'achievements')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionBaseSerializer(many=False, read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'context', 'is_correct', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerBaseSerializer(many=True, read_only=True)
    language = LanguageSerializer(many=False, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'context', 'external_source',
                  'language', 'question_type', 'answers',
                  'get_gap_markdown', 'difficulty')


class RoundSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Round
        fields = ('id', 'round_number', 'question')


class ChallengeSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=False, read_only=True)
    rounds = RoundSerializer(many=True)

    class Meta:
        model = Challenge
        fields = ('id', 'language', 'rounds')


class GivenAnswerSerializer(serializers.ModelSerializer):
    user = UserAchievementsSerializer(many=False, read_only=True)
    is_correct = serializers.BooleanField(source='answer.is_correct')
    
    class Meta:
        model = GivenAnswer
        fields = ('id', 'user', 'round', 'is_correct')
        

class ScoreSerializer(serializers.ModelSerializer):
    given_answers = GivenAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Score
        fields = ('id', 'status', 'challenge', 'given_answers')
