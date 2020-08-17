from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, default="")
    last_name = models.CharField(max_length=64, default="")
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=20)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Relation(models.Model):
    RELATIONS = [
        ('parent', 'Parent'),
        ('partner', 'Partner'),
        ('child', 'Child')
    ]

    relation_from = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='ralation_from')
    relation_to = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='ralation_to')
    relation = models.CharField(max_length=16, choices=RELATIONS, default=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
