from django.db import models
from django.conf import settings
from mptt.models import TreeForeignKey, MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.cache import cache
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.

class Favour(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favours')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return "{} 喜欢 {}_{}".format(self.user.username, self.content_object._meta.model_name, self.content_object.id)


class Comment(MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    post = models.ForeignKey(settings.COMMENT_ENTRY_MODEL, verbose_name='文章')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name='父级评论',)
    content = RichTextUploadingField(verbose_name='评论', config_name='comment')
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    favours = GenericRelation(Favour)

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
