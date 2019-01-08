from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet

from .models import Language, Achievement, UserFollowing, Statistic
from .serializers import (
    UserFullSerializer, LanguageSerializer, AchievementBaseSerializer,
    UserAchievementSerializer, UserBaseSerializer, StatisticSerializer
)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
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

    @action(detail=True, methods=['post'])
    def unfollow(self, request, *args, **kwargs):
        user = request.user
        following = self.get_object()
        user_following = get_object_or_404(UserFollowing, user=user, following=following)
        user_following.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def followings(self, request, *args, **kwargs):
        user = request.user
        followings = []
        for follow in user.following.all():
            followings.append(follow.following)
        serializer = UserBaseSerializer(followings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'put'])
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            user = request.user

            serializer = UserFullSerializer(user, context={"request": request}, many=False)
            return Response(serializer.data)
        elif request.method == 'PUT':
            user = request.user

            first_name = request.data.get('first_name', '')
            if first_name:
                user.first_name = first_name

            last_name = request.data.get('last_name', '')
            if last_name:
                user.last_name = last_name

            user.save()

            serializer = UserFullSerializer(user, context={"request": request}, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LanguageViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Language.objects.all().order_by('name')
    serializer_class = LanguageSerializer
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        serializer = LanguageSerializer(self.queryset, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        language = self.get_object()

        user.selected_languages.add(language)
        user.save()

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, *args, **kwargs):
        user = request.user
        language = self.get_object()

        user.selected_languages.remove(language)
        user.save()

        return Response(status=status.HTTP_201_CREATED)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementBaseSerializer
    authentication_classes = (TokenAuthentication,)


class StatisticsViewSet(GenericViewSet):
    serializer_class = StatisticSerializer
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['put'])
    def push(self, request, *args, **kwargs):
        user = request.user
        statistic = get_object_or_404(Statistic, user=user)
        card_count = request.data.get('correctly_swiped_taboo_cards', 0)
        translated_words = request.data.get('translated_words', 0)

        statistic.correctly_swiped_taboo_cards += card_count
        statistic.translated_words += translated_words

        statistic.save()

        return Response(status=status.HTTP_202_ACCEPTED)
