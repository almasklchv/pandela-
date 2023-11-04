from django.db import models
from blogs.models import Blog
from django.conf import settings

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comment")
    article = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE, related_name="blog_article")
    time = models.DateTimeField()
    content = models.CharField(max_length=300)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)


class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="user_reply")
    article = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE, related_name="parent_article")
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="parent_comment")
    time = models.DateTimeField()
    content = models.CharField(max_length=300)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class Reaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="user_like")
    article = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE, related_name="article")
    comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE, related_name="related_comment")
    reply = models.ForeignKey(Reply, null=True, on_delete=models.CASCADE, related_name="related_reply")
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


