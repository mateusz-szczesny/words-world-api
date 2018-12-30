from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
from django.http.response import HttpResponseNotFound
from rest_framework.viewsets import GenericViewSet

from .models import Language, Answer, Question, Achievement, Score, Round, GivenAnswer, Challenge, UserFollowing
from .serializers import (
    UserFullSerializer, LanguageSerializer, QuestionSerializer,
    AnswerSerializer, AchievementBaseSerializer, ScoreSerializer,
    ChallengeSerializer, RoundSerializer, GivenAnswerSerializer,
    UserBaseSerializer,UserAchievementSerializer,
    UserFollowingSerializer)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAchievementSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('id', 'username')
    search_fields = ('username', 'email')
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserAchievementSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        user = request.user
        if user:
            serializer = UserFullSerializer(user, many=False)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound('User not found')


class LanguageViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
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
            return Response([], status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, *args, **kwargs):
        user = request.user
        language = self.get_object()
        if language:
            user.selected_languages.remove(language)
            user.save()

            return Response('', status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponseNotFound('Language not found')


class UserFollowingVIewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    serializer_class = UserFollowingSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        followings = UserFollowing.objects.filter(user=user)
        return followings

    def create(self, request, *args, **kwargs):
        user = request.user
        following_id = request.data['user']
        following = get_object_or_404(User, pk=following_id)

        user_following = UserFollowing.objects.create(user=user, following=following)
        serializer = UserFollowingSerializer(user_following, many=False)
        return Response(serializer.data)


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


