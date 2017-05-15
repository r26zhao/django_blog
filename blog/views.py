from django.shortcuts import render, get_object_or_404
import logging
from django.conf import settings
from .models import *

logger = logging.getLogger('blog.views')


# Create your views here.

# 获得全局变量
def global_setting(request):
    return {'SITE_NAME': settings.SITE_NAME, 'SITE_DESCP': settings.SITE_DESCP, 'SITE_KEYWORDS': settings.SITE_KEYWORDS }


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.click_increase()
    tag_list = post.tag.all()
    title = post.title
    description = post.excerpt
    keywords = post.category.name
    for tag in tag_list:
        keywords = keywords + ', ' + tag.name
    return render(request, 'blog/detail.html', context={'post': post,
                                                        'title':title,
                                                        'keywords':keywords,
                                                        'description':description,})


def category(request):
    pass
