# Generated by Django 2.1.4 on 2018-12-16 00:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_language_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='selected_languages', to=settings.AUTH_USER_MODEL),
        ),
    ]