# Generated by Django 4.1.1 on 2022-09-19 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_remove_choice_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
