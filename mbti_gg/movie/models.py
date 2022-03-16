from django.db import models
from user.models import User
from mbti.models import Mbti

# Create your models here.
class Movie(models.Model):
    movie_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    user_id = models.ForeignKey('user.User', db_column='user_id', on_delete=models.CASCADE)
    mbti_id = models.ForeignKey('mbti.Mbti', db_column='mbti_id', on_delete=models.CASCADE, null=True)
    info = models.TextField(null=True, blank=True)
    photo = models.TextField(null=True, blank=True)
    
# create table movie_comment
class MovieComment(models.Model):
    m_cno = models.BigAutoField(primary_key=True)
    mbti_id = models.ForeignKey('mbti.Mbti', db_column='mbti_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey('user.User', db_column='user_id', on_delete=models.CASCADE)
    comment = models.TextField()
    
# create table movie_liked
class MovieLiked(models.Model):
    class Meta:
        unique_together = (('movie_id', 'user_id'))
    movie_id = models.ForeignKey('Movie', db_column='movie_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey('user.User', db_column='user_id', on_delete=models.CASCADE)