from django.db import models
from django.contrib import admin
from datetime import timedelta, datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default = datetime.now())
    
    def __str__(self):
        return self.question_text
    
    @admin.display(boolean=True, description='New')
    def was_published_recently(self):
        return self.pub_date + timedelta(days=1) > datetime.now() > self.pub_date

    @admin.display(boolean=True, description='Available')
    def has_options(self):
        return len(self.choice_set.all())>=2

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text