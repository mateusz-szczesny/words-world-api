from django.db import models
from django.contrib.auth.models import User

LEVEL = (
    ('E', 'EASY'),
    ('M', 'MEDIUM'),
    ('G', 'HARD'),
)


"""
    Language data model classes for lang definition and answer-question examples storing
"""


class Language(models.Model):
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(User, related_name='selected_languages')

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPE_OF_QUESTION = (
        ('GAP', 'Gap Filling'),
        ('IMG', 'Image'),
        ('MP3', 'Voice Recognition'),
    )

    GAP_MARKDOWN = "%_%"

    MAX_TIME = {
        'E': 90,
        'M': 60,
        'H': 30
    }

    DEFAULT_MAX_TIME = 60

    context = models.CharField(max_length=32)
    external_source = models.TextField(max_length=1024, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(
        max_length=3,
        choices=TYPE_OF_QUESTION
    )
    difficulty = models.CharField(max_length=1, choices=LEVEL, default='M')

    def get_gap_markdown(self):
        if self.question_type == 'GAP':
            return self.GAP_MARKDOWN
        else:
            return None

    def get_max_time(self):
        max_time = self.MAX_TIME.get(str(self.difficulty), self.DEFAULT_MAX_TIME)
        return max_time

    def __str__(self):
        return self.language.name + ' - ' + self.question_type + '(' + self.context + ')'


class Answer(models.Model):
    context = models.CharField(max_length=32)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return 'Ans: ' + str(self.context) + ' (' + str(self.is_correct) + ')'


"""
    Challenge logic for tournaments between users
"""


class Challenge(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='challenges')

    def __str__(self):
        return super().__str__() + str(self.language)


class Score(models.Model):
    GAME_STATUS = (
        ('IN PROGRESS', 'IN PROGRESS'),
        ('WON', 'WON'),
        ('LOST', 'LOST'),
        ('TIE', 'TIE'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    status = models.CharField(
        max_length=32,
        choices=GAME_STATUS
    )
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='summaries')

    def __str__(self):
        return '(' + str(self.status) + ') ' + str(self.challenge)


class Round(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='rounds')
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name='rounds')
    round_number = models.IntegerField()

    def __str__(self):
        return '(' + str(self.round_number) + ') ' + str(self.challenge)


class GivenAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_answers')
    answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='given_answers')
    score = models.ForeignKey(Score, on_delete=models.SET_NULL, related_name='given_answers', null=True, blank=True)

    def is_correct(self):
        return self.answer.is_correct


"""
    Achievement models 
"""


class Achievement(models.Model):
    condition = models.CharField(max_length=2048)
    name = models.CharField(max_length=128)
    font_awesome_icon = models.TextField(max_length=2048)
    users = models.ManyToManyField(User, related_name="achievements")

    def __str__(self):
        return str(self.name) + ' - ' + str(self.condition)


"""
    Extension for default User Model to implement relations between users
"""


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')

