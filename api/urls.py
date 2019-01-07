from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'languages', views.LanguageViewSet, base_name='languages')
router.register(r'achievements', views.AchievementViewSet, base_name='achievements')
router.register(r'statistics', views.StatisticsViewSet, base_name='statistics')

urlpatterns = [
    url('', include(router.urls)),
]
