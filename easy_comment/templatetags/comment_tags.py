from django import template
from ..forms import CommentForm
from ..models import Like
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
def get_comment_list_of(post):
    return post.comment_set.all()

@register.simple_tag
def get_comments_user_count(post):
    user_list = []
    for comment in post.comment_set.all():
        if not comment.user in user_list:
            user_list.append(comment.user)
    return len(user_list)

@register.simple_tag
def get_like_action(user, comment):
    if user.is_anonymous:
        return 0
    try:
        obj = Like.objects.get(user = user, comment = comment)
        return 1 if obj.status else -1
    except Like.DoesNotExist:
        return 0

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
    key1 = 'post_{}_comments'.format(post.id)
    html = cache.get(key1, None)
    if not html:
        html = ''
        comments = post.comment_set.all().order_by('-submit_date')
        for comment in comments:
            key = 'comment_{}_html'.format(comment.id)
            comment_html = cache.get(key, None)
            if not comment_html:
                comment_html = render_to_string('easy_comment/comment_entry.html', context={'comment': comment})
                cache.set(key, comment_html, timeout=300)
            html += comment_html
        cache.set(key1, html, timeout=300)
    return html
