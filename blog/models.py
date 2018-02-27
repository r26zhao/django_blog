from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.

# 用户模型.
# 第一种：采用的继承方式扩展用户信息（本系统采用）
# 扩展：关联的方式去扩展用户信息

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True, null=True, verbose_name='昵称')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    avatar = ProcessedImageField(upload_to='avatar', default='avatar/default.png', verbose_name='头像',
                                 processors=[ResizeToFill(85,85)],
                                 format='JPEG',
                                 options={'quality':60})

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if len(self.avatar.name.split('/')) == 1:
            self.avatar.name = self.username + '/' + self.avatar.name
        super(User, self).save(*args, **kwargs)

    def get_avatar_url(self):
        url = self.avatar.url
        file_name = url.split('/')[-1]
        if self.socialaccount_set.exists() and file_name == 'default.png':
            url = self.socialaccount_set.first().get_avatar_url()
        return url


# Tag 标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    slug = models.SlugField(max_length=50, default='', blank=False)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug':self.slug})

# Category 分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    slug = models.SlugField(max_length=50, default='', blank=False)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug':self.slug})

# Post 文章类
class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    excerpt = models.CharField(max_length=200, verbose_name='文章摘要')
    content = RichTextUploadingField(verbose_name='文章内容')
    click_count = models.PositiveIntegerField(default=0, verbose_name='点击次数')
    is_recommended = models.BooleanField(default=False, verbose_name='是否推荐')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    author = models.ForeignKey(User, verbose_name='作者')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    cover = ProcessedImageField(upload_to='cover', default='', verbose_name='封面', processors=[ResizeToFill(160, 120)],
                                format='JPEG',
                                options={"quality": 60})

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def click_increase(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

'''
# Comment 评论
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户')
    post = models.ForeignKey(Post, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
'''