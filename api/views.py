from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q

from .models import Language, UserFollowing, Statistic, TabooCard
from .serializers import (
    UserFullSerializer, LanguageSerializer, UserAchievementSerializer,
    UserBaseSerializer, StatisticSerializer, TabooCardSerializer)


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


class TabooCardViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       GenericViewSet):
    serializer_class = TabooCardSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.request.user.cards.all()

    @action(detail=False, methods=['get'])
    def random(self, request, *args, **kwargs):
        user = request.user
        count = request.query_params.get('card_count', 0)
        language_id = request.query_params.get('language_id', 0)
        cards = TabooCard.objects.all().filter(~Q(pk=user.pk), language__pk=language_id)[:int(count)]

        serializer = TabooCardSerializer(cards, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        language = get_object_or_404(Language, pk=request.data.get('language', 0))
        card = TabooCard(owner=user, times_shown=0, answered_correctly=0,
                         key_word=request.data.get('key_word'),
                         black_list=request.data.get('black_list'),
                         language=language)
        card.save()
        serializer = self.get_serializer(card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StatisticsViewSet(GenericViewSet):
    serializer_class = StatisticSerializer
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['put'])
    def push(self, request, *args, **kwargs):
        user = request.user
        statistic = get_object_or_404(Statistic, user=user)
        correctly_swiped_cards = request.data.get('correctly_swiped_cards', [])
        incorrectly_swiped_cards = request.data.get('incorrectly_swiped_cards', [])
        translated_words = request.data.get('translated_words', 0)

        statistic.correctly_swiped_taboo_cards += len(correctly_swiped_cards)
        statistic.swiped_taboo_cards += len(correctly_swiped_cards) + len(incorrectly_swiped_cards)
        statistic.translated_words += translated_words

        cards_to_update = TabooCard.objects.all().filter(pk__in=correctly_swiped_cards+incorrectly_swiped_cards)
        for card in cards_to_update:
            card.times_shown += 1
            if card.pk in correctly_swiped_cards:
                card.answered_correctly += 1
            card.save()
        statistic.save()

        return Response(status=status.HTTP_202_ACCEPTED)
