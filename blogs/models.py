import uuid

from django.db import models
from django.conf import settings

#МЕНЕДЖЕР - ЭТО РЕДАКТИРОВАНИЕ

# def blog_directory_path(instance,filename):
#     return 'blog/{0}/{1}' .format(instance.title,filename)
# ???? slug? pagination? pk?

class Blog(models.Model):

    class VideoObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_published=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=False, null=False)
    description = models.TextField(max_length=150, blank=True, null=True)
    #i deleted content and summary. content can be as a description
    video = models.FileField(upload_to='videos/', default=None) #new
    thumbnail = models.ImageField(upload_to="previews/", default="previews/defaultpreview.png", max_length=512) #new
    is_published = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likes", blank=True, symmetrical=False
    )
    saves = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="saves", blank=True, symmetrical=False
    )
    videoobjects = VideoObjects()
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    views = models.PositiveIntegerField(('views'), default=0)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ('-pub_date',)

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

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter(parent=instance)
        return qs

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    parent = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["-created_at", "-updated_at"]