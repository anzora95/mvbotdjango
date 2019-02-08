from django.db import models
from django.contrib.auth.models import User


# class UserInsta(models.Model):
# username_insta = models.CharField(max_length=30)
# password_insta = models.CharField(max_length=30)
class AppUser(User):
   insta_user = models.CharField(max_length=150)
   insta_pass = models.CharField(max_length=50)


   class Meta:
       verbose_name = 'AppUser'
       verbose_name_plural = 'AppUsers'

   def __str__(self):
       return '%s' % (self.username)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insta_user = models.CharField(max_length=150)
    insta_pass = models.CharField(max_length=50)
    

    class Meta:
        verbose_name = 'Cred'
        verbose_name_plural = 'Creds'

    def __str__(self):
        return '%s' % (self.insta_user)


class Comments(models.Model):
    insta_comment = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BlackList(models.Model):
    insta_black_list = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class HashtagList(models.Model):
    category = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'HashtagList'
        verbose_name_plural = 'HashtagLists'

    def __str__(self):
        return '%s' % (self.category)


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
    category = models.ForeignKey(HashtagList, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'List_Tag'
        verbose_name_plural = 'List_Tags'

    def __str__(self):
        return '%s' % (self.insta_tag)



class Features(models.Model):
    id_feature= models.IntegerField(primary_key=True)
    feature_name = models.CharField(max_length=100)


class ChildTag(models.Model):
    tag_name= models.CharField(max_length=100)
    hashtag_id = models.IntegerField(primary_key=True,)
    dad_tag = models.ForeignKey(HashtagList, on_delete=models.CASCADE)
#Lectura de hasgtags para el task

class Task(models.Model):
    creds=models.ForeignKey(Creds,on_delete=models.CASCADE)
    active=models.BooleanField()
    tags=models.CharField(max_length=1000)
    likemedia=models.BooleanField()
    followuser=models.BooleanField()
    dontlikemedia=models.BooleanField()
    dontfollow=models.BooleanField()
    randomlylike=models.BooleanField()
    search=models.BooleanField()
    antispamfilter=models.BooleanField()
    custowordfilter=models.BooleanField()
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return '%s' % (self.tags)

class LastLogin(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    cred=models.ForeignKey(Creds,on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'lastLogin'
        verbose_name_plural = 'lastLogin'

    def __str__(self):
        return '%s' % (self.user)

class thread(models.Model):
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    codigo=models.CharField(max_length=1000)
    class Meta:
        verbose_name = 'thread'
        verbose_name_plural = 'threads'

    def __str__(self):
        return '%s' % (self.task.tags)