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
        """Return boolean his function it will return true when poll is publish recently return true."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self) -> bool:
        """Return boolean if current date is on or after question’s publication date return true."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return boolean if voting is currently allowed for this question return true."""
        if self.end_date is None:
            return self.is_published()
        return self.pub_date <= timezone.now() <= self.end_date
    
    def __str__(self):
        """Return readable string name of question"""
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return readable string name of choice"""
        return self.choice_text
