from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    fields = (
                'title', 'cat', 'content', 'photo',
                'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True


    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50 height=40>")
        else:
            return "Нет фото"

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = 'Админ-панель сайта с рецептами'
admin.site.site_header = 'Админ-панель сайта с рецептами'
