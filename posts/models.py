from django.db import models
from django.contrib.auth.models import User


class PostCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    contents = models.TextField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(PostCategory,on_delete=models.SET_NULL,null=True)
    likes = models.ManyToManyField(User,related_name="post_likes")

    def number_of_likes(self):
        return self.likes.count()


class PostComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    contents = models.TextField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
