from django.db import models

# Create your models here.
class Notice(models.Model) :
    nno     = models.BigAutoField(primary_key=True)
    title   = models.CharField(max_length=200)
    writer  = models.CharField(max_length=100)
    content = models.TextField()
    regdate = models.DateTimeField(auto_now=True)
    viewcnt = models.IntegerField(default=0)


class NoticeWriting(models.Model) :
    n_cno     = models.BigAutoField(primary_key=True)
    txt    = models.CharField(max_length=500)
    writer = models.CharField(max_length=100)
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE)