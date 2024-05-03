from django.urls import path
from .views import LoginApiView,RegistrationAPIView,GetAllUsersView,PostListCreateView,UpdatePost,AddCommentView,AllCommentsView,AddLikeView,UsersWhoLikedPostView,FollowView,AcceptFriendRequestView

app_name='users'

urlpatterns=[
    path('login/',LoginApiView.as_view(), name='login'),
    path('register/',RegistrationAPIView.as_view(), name='register'),
    path('users/', GetAllUsersView.as_view(), name='get_all_users'),
    path('post/', PostListCreateView.as_view(), name='post'),
    path('post_update/', UpdatePost.as_view(), name='post_update'),
    path('add_comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
    path('comment_all/<int:id>/',AllCommentsView.as_view(), name='comment_all'),
    path('addlike/<int:pk>/',AddLikeView.as_view(), name='addlike'),
    path('all_like/<int:pk>/',UsersWhoLikedPostView.as_view(), name='all_like'),
    path('follower/<int:pk>/',FollowView.as_view(), name='follower'),
    path('followed/<int:id>/',AcceptFriendRequestView.as_view(), name='followed'),

]