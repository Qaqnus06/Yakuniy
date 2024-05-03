from rest_framework .views  import  APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer,RegistrationSerializer
from.models import User
from rest_framework import status,generics
from .serializers import UserSerializer 
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer,CommentSerializer
from .models import Post,Comment,Like,Follow



class LoginApiView(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user=authenticate(username=serializer.data['username'], password=serializer.data['password'])

        if user is None:
            data={
                "status":False,
                "message":"user not found"
            }

            return Response(data)
        refresh = RefreshToken.for_user(user)

        data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(data)
    
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            if User.objects.filter(username=username).exists():
                return Response({"message": "allaqachon bor "})
            
            user = User.objects.create_user(username=username, email=email,phone_number=phone_number, password=password)
            user.set_password(password)
            user.save()

            data = {
                "status": "success",
                "tokens":user.token()
            }
             
            return Response(data)
        return Response(user)   

class GetAllUsersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class UpdatePost(PostListCreateView):
    def update_post(self,instance,validate_data):
        instance.content=validate_data.get('content'.instance.content)
        permission_classes = [IsAuthenticated]
        instance.save()
        
        return instance

    
class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'})

        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data,)
        return Response(serializer.errors)   


class AllCommentsView(APIView):
    def get(self, request,id):
        if not Post.objects.filter(id=id).exists():
            return Response({'error': 'Post topilmadi'})

        commment = Comment.objects.all()  
        serializer = CommentSerializer(commment, many=True)
        return Response(serializer.data)


class AddLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            post =Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post topilmadi'})
        if post.likes.filter(id=request.user.id).exists():
            return Response({'error': 'Bu postga like bosgansiz'})
        post.likes.add(request.user)
        post.save()
        return Response({'message': 'Siz like bosdingiz'})
    
class UsersWhoLikedPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'})

        users = post.likes.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class FollowView(APIView):
    def post(self, request, pk):
        try:
            followed_user = User.objects.get(pk=pk) 
        except User.DoesNotExist:
            return Response({'error': 'User topilmadi'})

        if Follow.objects.filter(follower=request.user, followed=followed_user).exists():
            return Response({'error': 'Bu userga follow bosdingiz'})

        new_follow = Follow(follower=request.user, followed=followed_user)
        new_follow.save()

        return Response({'message': 'Siz follow bosdingiz'})

class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        friend_request = AcceptFriendRequestView.objects.get(pk=id, followed=request.user, is_active=False)
        if not friend_request:
            return Response({'error': 'dostlik sorovi yoq'})
        
        friend_request.is_active = True
        friend_request.save()
        return Response({'message': 'Dostingiz sorovngizni qabul qildi.'})   