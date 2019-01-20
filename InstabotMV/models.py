from django.db import models
from django.contrib.auth.models import User


# class UserInsta(models.Model):
# username_insta = models.CharField(max_length=30)
# password_insta = models.CharField(max_length=30)


class Media(models.Model):
    media_id = models.CharField(max_length=300)
    status = models.IntegerField()
    datetime = models.TextField()
    code = models.TextField()
    owner_name = models.CharField(max_length=100)


class Username(models.Model):
    username = models.CharField(max_length=300)
    username_id = models.CharField(max_length=300)
    unfollow_count = models.IntegerField()
    last_followed_time = models.TextField()


class Settings(models.Model):
    settings_name = models.TextField()
    settings_val = models.TextField()


class Creds(models.Model):
    insta_user = models.CharField(max_length=150)
    insta_pass = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    insta_comment = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BlackList(models.Model):
    insta_black_list = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class HashtagList(models.Model):
    id_tag = models.IntegerField(primary_key= True)
    catalogo = models.CharField(max_length=200)
    hashtag_names =models.TextField()


class UsList(models.Model):
    insta_us_name = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LocateList(models.Model):
    insta_locate = models.TextField()
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class List_Tag(models.Model):
    insta_tag = models.CharField(max_length=100)
    id_name = models.IntegerField()
    num_catalog = models.ForeignKey(HashtagList, on_delete=models.CASCADE)


class Features(models.Model):
    id_feature= models.IntegerField(primary_key=True)
    feature_name = models.CharField(max_length=100)


class ChildTag(models.Model):
    tag_name= models.CharField(max_length=100)
    hashtag_id = models.IntegerField(primary_key=True,)
    dad_tag = models.ForeignKey(HashtagList, on_delete=models.CASCADE)



