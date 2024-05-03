from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings




class User(AbstractUser):

    phone_number=models.CharField(max_length=13, unique=True, db_index=True)
    image=models.ImageField(upload_to="users/", default="users/default.jpeg")
    bio=models.TextField()
    def token(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='komentariya')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='komentariya')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

        

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='yoqtirishlar')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='yoqtirishlar')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.username + " useriga  "   + self.followed.username   +  "      obuna bo'ldi"  


