from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question = models.CharField(max_length=200)
    category = models.CharField(max_length=100, null=True)
    evaluation_id = models.CharField(null=True, max_length=255)
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self


class Evaluation(models.Model):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    lec_id = models.CharField(null=True, max_length=255)
    student_id = models.CharField(null=True, max_length=255)
    #question = models.ForeignKey(Question, related_name="payer_checked", on_delete=models.CASCADE, null=True)
    #question = ArrayField(ArrayField(models.IntegerField()))

    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self
