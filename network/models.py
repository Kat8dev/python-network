from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_likes")
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post.id
        }
    
    class Meta:
        unique_together = ("user", "post")
        
    def __str__(self):
        return f"{self.user} likes {self.post}"

        
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through=Like, blank=True, related_name="liked_posts")
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [like.username for like in self.likes.all()]  
        }
    
    def __str__(self):
        return f"{self.user} posted {self.content[:10]}"