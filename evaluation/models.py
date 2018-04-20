from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from users.models import User, Unit
from django.db.models import Q

RATINGS = (
    ('1', 'Poor'),
    ('2', 'Very Bad'),
    ('3', 'Bad'),
    ('4', 'Good'),
    ('5', 'Very Good'),
)


class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    student_id = models.ForeignKey(User, related_name="student", limit_choices_to=Q(role='student'),
                                   on_delete=models.CASCADE, null=True)
    lecturer_id = models.ForeignKey(User, related_name="lecturer", limit_choices_to=Q(role='lecturer'),
                                    on_delete=models.CASCADE, null=True)
    unit_id = models.ForeignKey(Unit, related_name="unit", on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        count = Evaluation.objects.count()
        super(Evaluation, self).save(*args, **kwargs)

    def dict(self):
        eval = {
            "id": self.id,
            "created": self.date_added,
            "student_id": self.student_id.id,
            "lecturer_id": self.lecturer_id.id,
            "unit_id": self.unit_id.id

        }

        return eval

    def lec_id(self):
        return str(self.lecturer_id.id)

    def stud_id(self):
        return str(self.student_id.id)

    def unit_id(self):
        return str(self.unit_id.id)

    def __unicode__(self):
        return "%s | %s" % (str(self.id), self.date_added)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question = models.CharField(max_length=200)
    category = models.CharField(max_length=100, null=True)
    evaluation_id = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=True)
    rating = models.CharField(max_length=30, choices=RATINGS, default='1')
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def eval_id(self):
        return str(self.evaluation_id.id)

    def __unicode__(self):
        return "%s %s" % (self.question, self.rating)




