from django.db import models
from user.models import *
from mbti.models import *

# Create your models here.

class Tour(models.Model):
    tour_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', default='admin')
    mbti_id = models.ForeignKey(Mbti, db_column='mbti_id', on_delete=models.CASCADE, null=True)
    info = models.TextField(null=True, blank=True)
    photo = models.TextField(null=True, blank=True)


class TourComment(models.Model):
    h_cno = models.BigAutoField(primary_key = True)
    mbti_id = models.ForeignKey(Mbti,on_delete=models.CASCADE, db_column='mbti_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    comment = models.TextField()


class TourLiked(models.Model):
    tour_id = models.ForeignKey(Tour, on_delete=models.CASCADE, db_column='tour_id')
    like_user = models.ManyToManyField(User, related_name='like_user_tour', blank=True)

    def total_like_user(self):
        return self.like_user.count()