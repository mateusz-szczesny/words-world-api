from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from .models import Language, Question, Answer, Achievement, Score, Challenge, GivenAnswer, Round, UserFollowing, \
    Statistic


class AchievementBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'font_awesome_icon', 'level', 'score')


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ('correctly_swiped_taboo_cards', 'translated_words')


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


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'required': True, 'write_only': True},
                        'first_name': {'read_only': True},
                        'last_name': {'read_only': True}}


class LanguageSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = ('id', 'name', 'is_subscribed', 'language_code')
        ordering = ('name', )

    def get_is_subscribed(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user in obj.users.all():
            return True
        else:
            return False


class UserAchievementSerializer(serializers.ModelSerializer):
    achievements = AchievementBaseSerializer(many=True, read_only=True)
    is_friend = serializers.SerializerMethodField()
    selected_languages = LanguageSerializer(many=True, read_only=True)
    overall_score = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'is_friend', 'overall_score',
                  'achievements', 'selected_languages')
        ordering = ('username', 'first_name', 'last_name')

    def get_overall_score(self, obj):
        return obj.achievements.all().aggregate(Sum('score'))

    def get_is_friend(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user:
            followings = []
            for follow in user.following.all():
                followings.append(follow.following)
            if obj in followings:
                return True
            else:
                return False
        else:
            return False


class UserFullSerializer(serializers.ModelSerializer):
    achievements = AchievementBaseSerializer(many=True, read_only=True)
    selected_languages = LanguageSerializer(many=True, read_only=True)
    following = serializers.SerializerMethodField()
    overall_score = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'overall_score', 'achievements',
                  'selected_languages', 'following')

    def get_overall_score(self, obj):
        return obj.achievements.all().aggregate(Sum('score'))

    def get_following(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user:
            followings = []
            for follow in user.following.all():
                followings.append(follow.following)
            serializer = UserBaseSerializer(followings, many=True)
            return serializer.data
        else:
            return []


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
    user = UserBaseSerializer(many=False, read_only=True)
    is_correct = serializers.BooleanField(source='answer.is_correct')
    
    class Meta:
        model = GivenAnswer
        fields = ('id', 'user', 'round', 'is_correct')
        

class ScoreSerializer(serializers.ModelSerializer):
    given_answers = GivenAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Score
        fields = ('id', 'status', 'challenge', 'given_answers')


class UserFollowingSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer(many=False)
    following = UserBaseSerializer(many=False)

    class Meta:
        model = UserFollowing
        fields = ('id', 'user', 'following')
