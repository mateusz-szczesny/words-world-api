from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Language
from .serializers import UserSerializer, LanguageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer

    def get_queryset(self):
        qs = Language.objects.order_by('name')
        return qs
