from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^category/(?P<name>[a-zA-Z0-9_\-\u4e00-\u9fa5]+)/$', views.category, name='category'),
    url(r'^search/$', views.search, name='search'),
]