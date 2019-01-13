from fractions import Fraction

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_blank_statistics(sender, instance=None, created=False, **kwargs):
    if created:
        Statistic.objects.create(user=instance)


class Language(models.Model):
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(User, related_name='selected_languages', blank=True)
    language_code = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Language):
            return self.name == other.name
        else:
            return False


class Achievement(models.Model):
    LEVEL_CHOICES = (
        ("1", "Bronze"),
        ("2", "Silver"),
        ("3", "Gold"),
        ("4", "Diamond"),
    )

    condition = models.TextField(max_length=2048)
    name = models.CharField(max_length=128)
    font_awesome_icon = models.TextField(max_length=2048)
    users = models.ManyToManyField(User, related_name="achievements", blank=True)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    score = models.IntegerField()

    def __str__(self):
        return str(self.name)

    def try_award_to(self, user):
        has_achievement = self in user.achievements.all()
        if has_achievement:
            return False
        condition_result = eval(str(self.condition))
        if condition_result:
            user.achievements.add(self)
            return True
        else:
            return False


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')


class Statistic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    correctly_swiped_taboo_cards = models.IntegerField(default=0)
    swiped_taboo_cards = models.IntegerField(default=0)
    translated_words = models.IntegerField(default=0)

    @property
    def taboo_efficiency(self):
        if self.swiped_taboo_cards is not 0:
            return Fraction(self.correctly_swiped_taboo_cards, self.swiped_taboo_cards)
        else:
            return 0


class TabooCard(models.Model):
    key_word = models.CharField(max_length=128)
    black_list = models.CharField(max_length=2048)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='cards')
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, related_name='cards')
    times_shown = models.IntegerField(default=0)
    answered_correctly = models.IntegerField(default=0)

    @property
    def difficulty(self):
        if self.times_shown is 0:
            return "NOT ENOUGH STATS"
        ratio = Fraction(self.answered_correctly, self.times_shown)
        if 0 <= ratio < 0.25:
            return "INSANE"
        elif 0.25 <= ratio < 0.5:
            return "HARD"
        elif 0.5 <= ratio < 0.75:
            return "MEDIUM"
        elif 0.75 <= ratio:
            return "EASY"

    @property
    def card_efficiency(self):
        if self.times_shown is not 0:
            return Fraction(self.answered_correctly, self.times_shown)
        else:
            return 0

    def __str__(self):
        return self.pk + ' | ' + self.key_word + ' | ' + self.language.language_code


@receiver(post_save, sender=Statistic)
@receiver(post_save, sender=UserFollowing)
@receiver(post_save, sender=User)
def trigger_achievements_after_statistics_save(sender, instance=None, created=False, **kwargs):
    if isinstance(instance, User):
        if not created:
            grant_achievements(instance)
    else:
        grant_achievements(instance.user)


def grant_achievements(user):
    for achievement in Achievement.objects.all():
        achievement.try_award_to(user)
