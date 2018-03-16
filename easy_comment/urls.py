from django.conf.urls import url
from . import views
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

app_name = 'easy_comment'
urlpatterns = [
    url(r'^post/submit-comment/$', login_required(require_POST(views.PostCommentView.as_view())), name='submit_comment'),
    url(r'^post/(?P<pk>\d+)/comments/', views.PostCommentView.as_view(), name='post_comments_list'),
    url(r'^post/(?P<post_id>\d+)/favours/$', views.PostFavourView.as_view(), name='post_favour_count'),
    url(r'^post/(?P<post_id>\d+)/change-favour/$', require_POST(views.PostFavourView.as_view()), name='post_favour'),
]