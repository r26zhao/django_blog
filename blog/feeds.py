from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class BlogFeed(Feed):
    title = 'Aaron Zhao的博客'
    link = '/'
    description = 'New posts of my blog.'

    def items(self):
        return Post.objects.all()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
