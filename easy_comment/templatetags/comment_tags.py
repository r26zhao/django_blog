from django import template
from ..models import Comment

register = template.Library()

@register.simple_tag
def get_comments(post):
    return post.comment_set.all()

@register.simple_tag
def get_comments_user_count(post):
    user_list = []
    for comment in post.comment_set.all():
        if not comment.user in user_list:
            user_list.append(comment.user)
    return len(user_list)