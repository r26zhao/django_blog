from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'excerpt', 'content', 'category', 'tag', 'author',)
    list_display = ('title', 'date_created', 'date_modified', 'category', 'author', 'is_recommended',)
    list_editable = ('category', 'author', 'is_recommended',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(User)