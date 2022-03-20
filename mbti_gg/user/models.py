from django.db import models
from django.db.models import Q


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    pwd = models.CharField(max_length=50)
    mbti_id = models.ForeignKey('mbti.Mbti', on_delete=models.PROTECT, db_column='mbti_id')
    birth_dt = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICES)
    # gender = models.CharField(max_length=1)
    #
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(check=Q(gender__in='M' or 'F'), name='gender')
    #     ]

