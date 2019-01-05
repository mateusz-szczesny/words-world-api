def grant_achievements(user):
    achievements = Achievement.objects.all()

    for achievement in achievements:
        if achievement not in user.achievements.all():
            pass
