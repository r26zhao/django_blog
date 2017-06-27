from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.conf import settings
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .forms import UserDetailForm
from django.contrib.auth.decorators import login_required


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
    title = post.title + ' - AA的博客'
    description = post.excerpt
    keywords = post.category.name
    for tag in tag_list:
        keywords = keywords + ', ' + tag.name
    return render(request, 'blog/detail.html', context={'post': post,
                                                        'title':title,
                                                        'keywords':keywords,
                                                        'description':description,
                                                        'tag_list':tag_list})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post_list = Post.objects.filter(category=category)
    post_list = get_page(request, post_list)
    title = category.name + ' - AA的博客'
    keywords = category.name
    description = category.name
    return render(request, 'blog/index.html', context={'post_list':post_list,
                                                       'title':title,
                                                       'keywords':keywords,
                                                       'description':description})

def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post_list = Post.objects.filter(tag__in=[tag])
    post_list = get_page(request, post_list)
    title = tag.name + ' - AA的博客'
    keywords = tag.name
    description = tag.name
    return render(request, 'blog/index.html', context={'post_list': post_list,
                                                       'title': title,
                                                       'keywords': keywords,
                                                       'description': description})

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/search.html', context={'error_msg':error_msg})
    post_list = Post.objects.filter(title__contains=q)
    post_list = get_page(request,post_list)
    return render(request, 'blog/search.html', context={'error_msg':error_msg, 'post_list':post_list})

@login_required
def account_profile(request):
    messages = []
    if request.method == 'POST':
        request_dic = getattr(request, 'POST')
        print(request_dic)
        print(request.FILES)
        form = UserDetailForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.append('资料修改成功！')
    form = UserDetailForm(instance=request.user)
    return render(request, 'account/user_detail.html', context={'form':form,
                                                                'messages':messages,})