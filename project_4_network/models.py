from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="social_profile")
    following = models.ManyToManyField('project_4_network.Profile', related_name="followers")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name="Liked_Posts", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "userid": self.user.id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [ user.id for user in self.likes.all()]
        }

    def __str__(self):
        return f"{self.user} Posted at {self.timestamp} with {self.likes.count()} likes"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented '{self.comment}' on {self.post}"
