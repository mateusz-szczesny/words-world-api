from django.db import models
from django.contrib.auth.models import User

"""
    Language data model classes for lang definition and answer-question examples storing
"""


class Language(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPE_OF_QUESTION = (
        ('GAP', 'Gap Filling'),
        ('IMG', 'Image'),
        ('MP3', 'Voice Recognition'),
    )

    GAP_MARKDOWN = "%_%"

    context = models.CharField(max_length=32)
    external_source = models.TextField(max_length=1024, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(
        max_length=3,
        choices=TYPE_OF_QUESTION
    )

    def get_gap_markdown(self):
        if self.question_type == 'GAP':
            return self.GAP_MARKDOWN
        else:
            return None

    def __str__(self):
        return self.language.name + ' - ' + self.question_type + '(' + self.context + ')'


class Answer(models.Model):
    context = models.CharField(max_length=32)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return 'Ans: ' + self.context + ' (' + str(self.is_correct) + ')'


"""
    Challenge logic for tournaments between users
"""


# class Challenge(models.Model):
#    pass


# class Round(models.Model):
#     pass


"""
    Achievement models 
"""


class Achievement(models.Model):
    condition = models.CharField(max_length=2048)
    name = models.CharField(max_length=128)
    font_awesome_icon = models.TextField(max_length=2048)
    users = models.ManyToManyField(User, related_name="achievements")

    def __str__(self):
        return self.name + ' - ' + self.condition


"""
    Extension for default User Model to implement relations between users
"""
