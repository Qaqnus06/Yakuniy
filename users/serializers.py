from rest_framework  import serializers
from .models import User,Post,Comment,Like,Follow

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=4)
    password = serializers.CharField(min_length=4)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=4, required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=13)
    password = serializers.CharField(max_length=20,required=True)
    confirm_password=serializers.CharField(max_length=20,required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class  PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post','user','content']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post','user','created_at']


class FolowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower','following','created_at']