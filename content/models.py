from django.db import models


class Feed(models.Model):
    email = models.EmailField(default='')
    image = models.TextField()
    content = models.TextField()


class Comment(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    content = models.TextField()


class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)


class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)
