from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogView.as_view(), name="blog"),
    path('post/<int:post_id>/', views.PostView.as_view(), name="post"),
    path('post/comment-reply/<int:post_id>/<int:comment_id>', views.CommentReplyView.as_view(), name="comment-reply"),
]
