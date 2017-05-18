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