from django import template
from ..models import *
from django.db.models.aggregates import Count
from django.core.cache import cache

register = template.Library()


@register.simple_tag
def get_category():
    category_list = Category.objects.annotate(post_num=Count('post')).order_by('-post_num')
    Category.objects.values()
    return category_list


@register.simple_tag
def get_tag():
    tag_list = Tag.objects.annotate(post_num=Count('post')).order_by('-post_num')
    return tag_list


@register.simple_tag
def get_reading_rank(num=5):
    post_list = Post.objects.all().order_by('-click_count')[:num]
    return post_list


@register.simple_tag
def get_recent_post(num=5):
    post_list = Post.objects.all()[:num]
    return post_list


@register.simple_tag
def get_blog_owner():
    owner = cache.get('owner', None)
    if not owner:
        from blog.models import User
        user = User.objects.get(id=1)
        post_num = len(user.post_set.all())
        view_num = 0
        for post in user.post_set.all():
            view_num += post.click_count
        owner = {'name': user.username, 'post_num': post_num, 'view_num': view_num, 'avatar': user.avatar.url}
        cache.set('owner', owner, timeout=24*60*60)
    return owner


@register.simple_tag
def get_friend_links():
    links = FriendLink.objects.all()
    return links
