from django.contrib import admin
from blog import models
from .models import Comment

admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'jalali_date', 'status',)
    list_filter = ('title', 'author','status',)
    search_fields=('title',)
    
admin.site.register(models.Post, PostAdmin)

