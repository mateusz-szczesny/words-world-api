from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters

from .models import Language, Answer, Question, Achievement, Score, Round, GivenAnswer, Challenge
from .serializers import UserSerializer, LanguageSerializer, QuestionSerializer, AnswerSerializer, \
    AchievementBaseSerializer, ScoreSerializer, ChallengeSerializer, RoundSerializer, GivenAnswerSerializer, \
    UserFollowingSerializer, UserBaseSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserBaseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('id', 'username')
    search_fields = ('username', 'email')

    @action(detail=False, methods=['get'])
    def following(self, request, **kwargs):
        user = request.user
        followings = user.following.all()
        serializer = UserFollowingSerializer(followings, many=True)
        return Response(serializer.date)

    @action(detail=False, methods=['get'])
    def followed(self, request, **kwargs):
        user = request.user
        followings = user.followed_by.all()
        serializer = UserFollowingSerializer(followings, many=True)
        return Response(serializer.date)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response(serializer.data)


class LanguageViewSet(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer

    def get_queryset(self):
        qs = Language.objects.order_by('name')
        return qs


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
    queryset = Round.objects.all()
    serializer_class = RoundSerializer


class GivenAnswerViewSet(viewsets.ModelViewSet):
    queryset = GivenAnswer.objects.all()
    serializer_class = GivenAnswerSerializer


