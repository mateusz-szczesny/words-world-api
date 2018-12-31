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
    UserAchievementSerializer, UserFollowingSerializer, UserBaseSerializer)


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
        serializer = UserAchievementSerializer(instance, context={"request": request}, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwargs):
        user = request.user
        new_following = self.get_object()
        following = get_object_or_404(User, pk=new_following.pk)
        UserFollowing.objects.create(user=user, following=following)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def followings(self, request, *args, **kwargs):
        user = request.user
        if user:
            followings = []
            for follow in user.following.all():
                followings.append(follow.following)
            serializer = UserBaseSerializer(followings, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get', 'put'])
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            user = request.user
            if user:
                serializer = UserFullSerializer(user, context={"request": request}, many=False)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PUT':
            user = request.user
            first_name = request.data.get('first_name', '')
            if first_name:
                user.first_name = first_name
            last_name = request.data.get('last_name', '')
            if last_name:
                user.last_name = last_name
            user.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LanguageViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Language.objects.order_by('name')
    serializer_class = LanguageSerializer
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        serializer = LanguageSerializer(self.queryset, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        language = self.get_object()
        if language:
            user.selected_languages.add(language)
            user.save()

            return Response(status=status.HTTP_201_CREATED)
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
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, *args, **kwargs):
        user = request.user
        language = self.get_object()
        if language:
            user.selected_languages.remove(language)
            user.save()

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


"""
TODO: Implement Challenge logic
"""


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


