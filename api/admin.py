from django.contrib import admin
from .models import Language, Question, Answer, Achievement, Challenge, Round, Score, GivenAnswer

admin.site.register(Language)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Achievement)
admin.site.register(Challenge)
admin.site.register(Round)
admin.site.register(Score)
admin.site.register(GivenAnswer)
