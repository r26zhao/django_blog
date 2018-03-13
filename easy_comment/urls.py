from django.conf.urls import url
from . import views

app_name = 'easy_comment'
urlpatterns = [
    url(r'^comment/like/$', views.like, name='like'),
    url(r'^post/submit-comment/$', views.PostCommentView.as_view(), name='submit_comment'),
    url(r'^post/(?P<pk>\d+)/comments/', views.PostCommentView.as_view(), name='post_comments_list'),
    url(r'^comment/(?P<pk>\d+)/like_dislikes/$', views.CommentLikeView.as_view(), name='comment_like'),
]