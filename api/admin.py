from django.contrib import admin
from .models import Language, Achievement, UserFollowing, Statistic, TabooCard

admin.site.register(Language)
admin.site.register(Achievement)
admin.site.register(UserFollowing)
admin.site.register(Statistic)
admin.site.register(TabooCard)
