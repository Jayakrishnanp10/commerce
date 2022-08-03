from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class listing(models.Model):
    title=models.CharField(max_length=100)
    desc=models.CharField(max_length=2000)
    sbid=models.FloatField(default=0)
    img=models.URLField()
    cbid=models.FloatField(default=sbid)
    bidder=models.ForeignKey(User, on_delete=models.CASCADE, related_name="biduser")
    seller=models.ForeignKey(User, on_delete=models.CASCADE, related_name="selluser")
    date=models.DateTimeField(default=datetime.now(), blank=True)
    categories=models.CharField(max_length=200)
    winner=models.ForeignKey(User, on_delete=models.CASCADE, related_name="wonuser")
    closed=models.BooleanField(default=False)
    watcher=models.ForeignKey(User, on_delete=models.CASCADE,null=True)

class bid(models.Model):
    bidlist=models.ForeignKey(listing,on_delete=models.CASCADE, related_name="bidding")
    bidded=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidlister")
    

class comment(models.Model):
    comment=models.CharField(max_length=1000)
    item=models.ForeignKey(listing,on_delete=models.CASCADE, related_name="itemcomment")
    date=models.DateTimeField(default=datetime.now(), blank=True)
    commenter=models.ForeignKey(User,on_delete=models.CASCADE, related_name="comuser")



