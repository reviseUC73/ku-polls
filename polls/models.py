from operator import truediv
from django.db import models
import datetime

from django.db import models
from django.utils import timezone
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('data end',null=True)

    def __str__(self):
        """Return name of question"""
        return self.question_text

    def was_published_recently(self):
        """This function it will return true when poll is publish recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return True if current date is on or after question’s publication date."""
        now = timezone.now
        return now >= self.pub_date

    def can_vote(self):
        """Return True if voting is currently allowed for this question."""
        now = timezone.now()
        return self.end_date >= now >= self.pub_date


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
