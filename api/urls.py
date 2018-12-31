from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'languages', views.LanguageViewSet, base_name='languages')

router.register(r'questions', views.QuestionViewSet, base_name='questions')
router.register(r'answers', views.AnswerViewSet, base_name='answers')
router.register(r'achievements', views.AchievementViewSet, base_name='achievements')
router.register(r'scores', views.ScoreViewSet, base_name='scores')
router.register(r'challenge', views.ChallengeViewSet, base_name='challenge')
router.register(r'rounds', views.RoundViewSet, base_name='rounds')
router.register(r'given_answers', views.GivenAnswerViewSet, base_name='given_answers')

urlpatterns = [
    url('', include(router.urls)),
]
