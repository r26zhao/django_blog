from django import template
from ..forms import CommentForm
from django.conf import settings
from django.apps import apps
from django.db.models.aggregates import Count
from django.core.cache import cache
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def generate_form_for(post):
    form = CommentForm(initial={'post':post.id})
    return form

@register.simple_tag
def get_comments_count(post):
    key = "post_{}_comments_num".format(post.id)
    comment_num = cache.get(key, None)
    if not comment_num:
        comment_num = post.comment_set.all().count()
        cache.set(key, comment_num, timeout=300)
    return comment_num

@register.simple_tag
def get_comments_user_count(post):
    key = "post_{}_comments_user_num".format(post.id)
    user_num = cache.get(key, None)
    if not user_num:
        user_list = []
        key1 = "post_{}_comments_user".format(post.id)
        for comment in post.comment_set.all():
            if not comment.user in user_list:
                user_list.append(comment.user)
        user_num = len(user_list)
        cache.set(key, user_num, timeout=300)
        cache.set(key1, user_list, timeout=300)
    return user_num

@register.simple_tag
def get_like_count(comment):
    return comment.like_set.filter(status = True).count()

@register.simple_tag
def get_dislike_count(comment):
    return -comment.like_set.filter(status = False).count()

@register.simple_tag
def get_comment_rank(num=5):
    app_model = settings.COMMENT_ENTRY_MODEL.split('.')
    Post = apps.get_model(*app_model)
    post_list = Post.objects.annotate(comment_num=Count('comment')).order_by('-comment_num')
    return post_list[:num]

@register.simple_tag
def generate_comment_list(post):
    return post.to_comments_html()
