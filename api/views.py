from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import filters
from django.http.response import HttpResponseNotFound
from rest_framework.viewsets import GenericViewSet

from .models import Language, Answer, Question, Achievement, Score, Round, GivenAnswer, Challenge
from .serializers import (
    UserAchievementsSerializer, LanguageSerializer, QuestionSerializer,
    AnswerSerializer, AchievementBaseSerializer, ScoreSerializer,
    ChallengeSerializer, RoundSerializer, GivenAnswerSerializer,
    UserBaseSerializer
)


class SignUpView(mixins.CreateModelMixin,
                 GenericViewSet):
    serializer_class = UserBaseSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserBaseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('id', 'username')
    search_fields = ('username', 'email')
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['get'])
    def following(self, request, *args, **kwargs):
        user = request.user
        followings = user.following.all()
        followed_users = []
        for follow in followings:
            followed_users.append(follow.following)
        serializer = UserBaseSerializer(followed_users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserAchievementsSerializer(instance)
        return Response(serializer.data)

    # TODO: add endpoint for adding user's follows


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.order_by('name')
    serializer_class = LanguageSerializer
    authentication_classes = (TokenAuthentication,)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        language = self.get_object()
        if language:
            user.selected_languages.add(language)
            user.save()

            serializer = LanguageSerializer(language, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return HttpResponseNotFound('Language not found')

    @action(detail=False, methods=['get'])
    def get_subscribed(self, request, *args, **kwargs):
        user = request.user
        languages = user.selected_languages.all()
        if languages.count() > 0:
            serializer = LanguageSerializer(languages, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound()


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementBaseSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all().order_by('round_number')
    serializer_class = RoundSerializer


class GivenAnswerViewSet(viewsets.ModelViewSet):
    queryset = GivenAnswer.objects.all()
    serializer_class = GivenAnswerSerializer


