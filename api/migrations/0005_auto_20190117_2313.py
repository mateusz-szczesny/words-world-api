# Generated by Django 2.1.4 on 2019-01-17 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190112_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='ans_flashcards',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistic',
            name='correctly_ans_flashcards',
            field=models.IntegerField(default=0),
        ),
    ]
