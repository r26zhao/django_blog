from django.shortcuts import render, get_object_or_404
import logging
from django.conf import settings
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

logger = logging.getLogger('blog.views')


# Create your views here.

# Paginator function
def get_page(request, post_list):
    paginator = Paginator(post_list, 8)
    page = request.GET.get('page', 1)
    try:
        post_list = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        post_list = paginator.page(1)
    return post_list

# 获得全局变量
def global_setting(request):
    return {'SITE_NAME': settings.SITE_NAME, 'SITE_DESCP': settings.SITE_DESCP, 'SITE_KEYWORDS': settings.SITE_KEYWORDS }


def index(request):
    post_list = Post.objects.all()
    post_list = get_page(request, post_list)
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
                                                        'description':description,
                                                        'tag_list':tag_list})


def category(request, name):
    category = get_object_or_404(Category, name=name)
    post_list = Post.objects.filter(category=category)
    post_list = get_page(request, post_list)
    return render(request, 'blog/index.html', context={'post_list':post_list})

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/search.html', context={'error_msg':error_msg})
    post_list = Post.objects.filter(title__contains=q)
    post_list = get_page(request,post_list)
    return render(request, 'blog/search.html', context={'error_msg':error_msg, 'post_list':post_list})