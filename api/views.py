from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Language, Answer, Question, Achievement
from .serializers import UserSerializer, LanguageSerializer, QuestionSerializer, AnswerSerializer, \
    AchievementBaseSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


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
    queryset = Achievement.objects.all().order_by('-date_joined')
    serializer_class = AchievementBaseSerializer
