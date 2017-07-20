from django.db import models
from blog.models import User, Post
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Comment(MPTTModel):
    user = models.ForeignKey(User, blank=True, null=True, related_name='comments')
    user_name = models.CharField(blank=True, max_length=50, null=True)
    post = models.ForeignKey(Post, verbose_name='文章')
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name='父级评论')
    content = RichTextUploadingField(verbose_name='评论', config_name='comment',)
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    class MPTTMeta:
        order_insertion_by = ['submit_date']

    def __str__(self):
        if self.parent is not None:
            return '%s --> %s' % (self.user.username, self.parent.user.username)
        return 'post_%s___%s' % (str(self.post.id), self.user.username)