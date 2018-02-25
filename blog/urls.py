from django.conf.urls import url
from . import views
from .feeds import BlogFeed

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^category/(?P<slug>[a-zA-Z0-9_\-\u4e00-\u9fa5]+)/$', views.category, name='category'),
    url(r'^tag/(?P<slug>[a-zA-Z0-9_\-\u4e00-\u9fa5]+)/$', views.tag, name='tag'),
    url(r'^search/$', views.search, name='search'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
    url(r'^feeds/$', BlogFeed(), name='rss_feed')
]