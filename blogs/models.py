import uuid

from django.db import models
from django.conf import settings


#КАТЕГОРИИ
# from djangoblog.utils import cache_decorator ПИЗДАРИКИ КОНЕЧНО НО ВОТ ССЫЛКА С ЭТИМИ ПЛЕЦЛИСТАМИ СТРАШНЫМИ https://github.com/liangliangyy/DjangoBlog/blob/master/djangoblog/utils.py
#МЕНЕДЖЕР - ЭТО РЕДАКТИРОВАНИЕ
from django.urls import reverse

# def blog_directory_path(instance,filename):
#     return 'blog/{0}/{1}' .format(instance.title,filename)
# ???? slug? pagination? pk?



# class BaseModel(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)
#     pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
#     mod_date = models.DateTimeField(auto_now=True, auto_now_add=False)

#     # def save(self, *args, **kwargs):
#     #     is_update_views = isinstance(
#     #         self,
#     #         Blog) and 'update_fields' in kwargs and kwargs['update_fields'] == ['views']
#     #     if is_update_views:
#     #         Blog.objects.filter(pk=self.pk).update(views=self.views)
#     #     else:
#     #         if 'slug' in self.__dict__:
#     #             slug = getattr(
#     #                 self, 'title') if 'title' in self.__dict__ else getattr(
#     #                 self, 'name')
#     #             setattr(self, 'slug', slugify(slug))
#     #         super().save(*args, **kwargs)
#
#     class Meta:
#         abstract = True
#         ordering = ('-pub_date',)

class Blog(models.Model):

    class VideoObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_published=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=False, null=False)
    description = models.TextField(max_length=1500, blank=True, null=True)
    #i deleted content and summary. content can be as a description
    video = models.FileField(upload_to='videos/', default=None) #new
    thumbnail = models.ImageField(upload_to="previews/", default="previews/defaultpreview.png", max_length=512) #new
    is_published = models.BooleanField(default=True)
    # pub_date = models.DateTimeField(auto_now_add=True)
    # mod_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likes", blank=True, symmetrical=False
    )
    saves = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="saves", blank=True, symmetrical=False
    )
    videoobjects = VideoObjects()
    views = models.PositiveIntegerField(('views'), default=0)
    playlist_setting = models.ForeignKey(
        'Playlist',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-pub_date", "-mod_date"]

    def __str__(self):
        return self.title + " ({})".format(self.author.username)

    def author_pname(self):
        return self.author.username

    def no_of_likes(self):
        if self.likes.count():
            if self.likes.count() == 1:
                return self.likes.count()
            return self.likes.count()
        return 0

    def get_video(self):
        if self.video:
            return self.video.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''

    # @cache_decorator(60 * 60 * 10)
    # def get_category_tree(self):
    #     tree = self.category.get_category_tree()
    #     names = list(map(lambda c: (c.name, c.get_absolute_url()), tree))
    #
    #     return names

    @property
    def comments(self):
        instance = self
        qs = Comment.videoobjects.filter(parent=instance)
        return qs

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    parent = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    #честно ну на всякиц случай пусть будет айдишник у комма

    class Meta:
        ordering = ["-pub_date", "-mod_date"]

class Playlist(models.Model):
    name = models.CharField('Название Плейлиста', max_length=30, unique=True)
    description = models.TextField(max_length=1500, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        blank=True,
        null=True)
    videos = models.ManyToManyField("Blog", blank=True)
    thumbnail = models.ImageField(upload_to="previews/", default="previews/defaultpreview.png", max_length=512)  # new
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True, auto_now_add=False)


    #add thumbnail and description. delete slug and add cool index or delete indel just -pub_date
    class Meta:
        ordering = ['-pub_date']
        verbose_name = ('Плейлист')
        verbose_name_plural = ('Плейлист')

    # def get_absolute_url(self):
    #     return reverse(
    #         'blog:playlist_detail', kwargs={
    #             'playlist_name': self.slug})

    def __str__(self):
        return self.name


    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''

    # @cache_decorator(60 * 60 * 10)
    # def get_playlist_tree(self):
    #     """
    #     递归获得分类目录的父级
    #     :return:
    #     """
    #     playlists = []
    #
    #     def parse(category):
    #         playlists.append(category)
    #         if playlist.parent_playlist:
    #             parse(category.parent_category)
    #
    #     parse(self)
    #     return categorys
    #

# sub_category стоит убрать хрень какая-то
#     @cache_decorator(60 * 60 * 10)
#     def get_sub_categorys(self):
#         """
#         获得当前分类目录所有子集
#         :return:
#         """
#         categorys = []
#         all_categorys = Category.objects.all()
#
#         def parse(category):
#             if category not in categorys:
#                 categorys.append(category)
#             childs = all_categorys.filter(parent_category=category)
#             for child in childs:
#                 if category not in categorys:
#                     categorys.append(child)
#                 parse(child)
#
#         parse(self)
#         return categorys


