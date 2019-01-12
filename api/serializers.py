from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from .models import Language, Achievement, Statistic, TabooCard


class AchievementBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'font_awesome_icon', 'level', 'score')


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ('correctly_swiped_taboo_cards', 'translated_words')


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'required': True, 'write_only': True},
                        'first_name': {'read_only': True},
                        'last_name': {'read_only': True}}


class LanguageMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name', 'language_code')
        ordering = ('name', )


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
    taboo_efficiency = serializers.FloatField(source='statistics.taboo_efficiency', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'overall_score', 'taboo_efficiency',
                  'achievements', 'selected_languages', 'following')

    def get_overall_score(self, obj):
        return obj.achievements.all().aggregate(Sum('score'))

    def get_following(self, obj):
        followings = []
        for follow in obj.following.all():
            followings.append(follow.following)
        serializer = UserBaseSerializer(followings, many=True)
        return serializer.data


class TabooCardSerializer(serializers.ModelSerializer):
    black_list = serializers.SerializerMethodField()
    difficulty = serializers.CharField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    language = LanguageMiniSerializer(many=False, read_only=True)
    card_efficiency = serializers.FloatField(read_only=True)

    class Meta:
        model = TabooCard
        fields = ('id', 'key_word', 'black_list', 'card_efficiency',
                  'difficulty', 'owner', 'language',
                  'times_shown', 'answered_correctly')

    def get_black_list(self, obj):
        return str(obj.black_list).split(';')
