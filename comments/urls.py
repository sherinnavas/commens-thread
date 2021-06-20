from django.urls import path
from comments.views import *

urlpatterns = [
    path('comment/<int:pk>/', CommentView.as_view(),name='comment_actions'),
    path('comments/create/<int:post_id>', CommentCreateView.as_view(), name='comment_create'),
    path('comments/view/<int:post_id>', CommentList.as_view(), name='comments_list'),
]
