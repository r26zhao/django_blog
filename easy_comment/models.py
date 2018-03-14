from django.db import models
from django.conf import settings
from mptt.models import TreeForeignKey, MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.cache import cache
from django.template.loader import render_to_string

# Create your models here.

class Comment(MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    post = models.ForeignKey(settings.COMMENT_ENTRY_MODEL, verbose_name='文章')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='父级评论',)
    content = RichTextUploadingField(verbose_name='评论', config_name='comment')
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comments_liked')
    users_dislike = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comments_disliked')

    class MPTTMeta:
        order_insertion_by = ['submit_date']

    def __str__(self):
        if self.parent is not None:
            return '%s 回复 %s' % (self.user_name, self.parent.user_name)
        return '%s 评论文章 post_%s' % (self.user_name, str(self.post.id))

    def to_html(self, update=False):
        key = "comment_{}_html".format(self.id)
        html = cache.get(key)
        if html is None or update:
            html = render_to_string('easy_comment/comment_entry.html', context={'comment': self})
            cache.set(key, html, timeout=300)
        return html

    def likes_count(self, update=False):
        key = 'comment_{}_likes'.format(self.id)
        result = cache.get(key)
        if update or result is None:
            result = {}
            result['likes'] = self.users_like.all().count()
            result['dislikes'] = -self.users_dislike.all().count()
            cache.set(key, result, timeout=300)
        return result