from django.db import models
from user.models import *
from mbti.models import *

# Create your models here.

class Hobby(models.Model):
    hobby_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', default='admin')
    info = models.TextField(null=True, blank=True)
    photo = models.TextField(null=True, blank=True)


class HobbyComment(models.Model):
    h_cno = models.BigAutoField(primary_key = True)
    mbti_id = models.ForeignKey(Mbti,on_delete=models.CASCADE, db_column='mbti_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    comment = models.TextField()


class HobbyLiked(models.Model):
    hobby_id = models.ForeignKey(Hobby, on_delete=models.CASCADE, db_column='hobby_id')
    like_user = models.ManyToManyField(User, related_name='like_user', blank=True)

    def total_like_user(self):
        return self.like_user.count()