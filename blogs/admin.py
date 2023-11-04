from django.contrib import admin
from .models import Comment, Blog, Playlist

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy  as _


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Playlist)

class BlogListFilter(admin.SimpleListFilter):
    title = ("author")
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = list(set(map(lambda x: x.author, Blog.videoobjects.all())))
        for author in authors:
            yield (author.id, (author.username))

    def queryset(self, request, queryset):
        id = self.value()
        if id:
            return queryset.filter(author__id__exact=id)
        else:
            return queryset

class BlogForm(forms.ModelForm):
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'title')
    form = BlogForm
    list_display = (
        'id',
        'title',
        'author',
        'playlist_setting',
        'pub_date',
        'mod_date',
        'views',)
    list_display_links = ('id', 'title')
    # list_filter = (BlogListFilter, 'playlist_setting')
    # exclude = ('creation_time', 'last_modify_time')
    view_on_site = True


    def get_form(self, request, obj=None, **kwargs):
        form = super(BlogAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].queryset = get_user_model(
        ).objects.filter(is_superuser=True)
        return form

    def save_model(self, request, obj, form, change):
        super(BlogAdmin, self).save_model(request, obj, form, change)

    def get_view_on_site_url(self, obj=None):
        if obj:
            url = obj.get_full_url()
            return url
        # else:
        #     from youtube_new.utils import get_current_site
        #     site = get_current_site().domain
        #     return site
