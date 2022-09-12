from operator import truediv
from django.db import models
import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True)

    def was_published_recently(self):
        """This function it will return true when poll is publish recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self) -> bool:
        """Return True if current date is on or after question’s publication date."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return True if voting is currently allowed for this question."""
        if self.end_date is None:
            return self.is_published()
        return self.pub_date <= timezone.now() <= self.end_date
    
    def __str__(self):
        """Return name of question"""
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
