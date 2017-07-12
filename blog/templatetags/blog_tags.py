from django import template
from ..models import *
from  django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_category():
    category_list = Category.objects.annotate(post_num = Count('post')).order_by('-post_num')
    Category.objects.values()
    return category_list

@register.simple_tag
def get_tag():
    tag_list = Tag.objects.all()
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
def get_comment_rank(num=5):
    post_list = Post.objects.annotate(comment_num = Count('comment')).order_by('-comment_num')
    return post_list[:num]