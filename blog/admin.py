from django.contrib import admin
from .models import *
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'excerpt', 'content', 'category', 'tag', 'author', 'cover')
    list_display = ('title', 'date_created', 'date_modified', 'category', 'author', 'is_recommended',)
    list_editable = ('category', 'author', 'is_recommended',)


class TagAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class FriendLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User)
admin.site.register(FriendLink)
