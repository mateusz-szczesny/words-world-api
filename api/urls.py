from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'languages', views.LanguageViewSet, base_name='languages')
router.register(r'statistics', views.StatisticsViewSet, base_name='statistics')
router.register(r'taboo/cards', views.TabooCardViewSet, base_name='taboo_cards')
router.register(r'flashcards', views.FlashCardViewSet, base_name='flashcards')

urlpatterns = [
    url('', include(router.urls)),
    path('words/random', views.RandomWordView.as_view()),
]
