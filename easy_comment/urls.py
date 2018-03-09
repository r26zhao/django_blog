from django.conf.urls import url
from . import views

app_name = 'easy_comment'
urlpatterns = [
    url(r'^comment/like/$', views.like, name='like'),
    url(r'^post/submit-comment/$', views.PostCommentView.as_view(), name='submit_comment'),
]