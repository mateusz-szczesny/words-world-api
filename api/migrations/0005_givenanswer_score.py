# Generated by Django 2.1.4 on 2018-12-15 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20181215_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='givenanswer',
            name='score',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='given_answers', to='api.Score'),
        ),
    ]