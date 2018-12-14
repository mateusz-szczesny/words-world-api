from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'languages', views.LanguageViewSet, base_name='languages')
router.register(r'questions', views.QuestionViewSet, base_name='questions')
router.register(r'answers', views.AnswerViewSet, base_name='answers')
router.register(r'achievements', views.AchievementViewSet, base_name='achievements')

urlpatterns = [
    url('', include(router.urls)),
]
