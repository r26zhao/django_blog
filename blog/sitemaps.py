from django.contrib.sitemaps import Sitemap
from .models import Post, Category, Tag

class PostSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'
    def items(self):
        return Post.objects.all()
    def lastmod(self, obj):
        return obj.date_modified

class CategorySitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.post_set.all()[0].date_created

class TagSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return obj.post_set.all()[0].date_created