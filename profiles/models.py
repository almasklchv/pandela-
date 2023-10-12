import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from blogs.models import Blog
from django.shortcuts import reverse


class ProfileManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not name:
            raise ValueError("Пользователь должен иметь Имя и Фамилию")
        if not email:
            raise ValueError("У пользователя должна быть почта")
        user = self.model(
            name=name.capitalize(),
            email=self.normalize_email(email),
            username=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        print("Пользователь создан!")
        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(name=name, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Profile(AbstractUser):
    name = models.CharField("Имя и Фамилия", max_length=100)
    email = models.EmailField("Email", max_length=100, unique=True)
    username = models.CharField("Никнейм", max_length=100, unique=True)
    bio = models.TextField("Описание", blank=True)
    shapka = models.ImageField(
        "Шапка Профиля", upload_to="shapki/", default=None, null=True, blank=True, max_length=512)
    dp = models.ImageField(
        "Аватарка", upload_to="profiles/", default="avatars/profile.png"
    )
    # number_views = models.PositiveIntegerField(('number_views'), default=0)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="Follower", blank=True, symmetrical=False
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="Following",
        blank=True,
        symmetrical=False,
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    main_name = models.CharField("Название ссылки", max_length=100, blank=True, null=True)
    main_link = models.URLField(
        "Главная Ссылка",
        max_length=128,
        db_index=True,
        unique=True,
        blank=True, null=True
    )
    second_name = models.CharField("Имя и Фамилия", max_length=100, blank=True, null=True)
    second_link = models.URLField(
        "2 Ссылка",
        max_length=128,
        db_index=True,
        unique=True,
        blank=True, null=True
    )
    third_name = models.CharField("Имя и Фамилия", max_length=100, blank=True, null=True)
    third_link = models.URLField(
        "3 Ссылка",
        max_length=128,
        db_index=True,
        unique=True,
        blank=True, null=True
    )
    fourth_name = models.CharField("Имя и Фамилия", max_length=100, blank=True, null=True)
    fourth_link = models.URLField(
        "4 Ссылка",
        max_length=128,
        db_index=True,
        unique=True,
        blank=True, null=True
    )
    fifth_name = models.CharField("Имя и Фамилия", max_length=100, blank=True, null=True)
    fifth_link = models.URLField(
        "5 Ссылка",
        max_length=128,
        db_index=True,
        unique=True,
        blank=True, null=True
    )
    # is_active = models.BooleanField(default=True)
    # is_email_verified = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email



    def no_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        return 0

    # def videos(self): my code
    #     self.number_views = self.blog_set.count()
    #     self.save(update_fields=['number_views'])

    def no_of_following(self):
        if self.following.count():
            return self.following.count()
        return 0

    def no_of_blogs(self):
        if self.blog_set.count():
            return self.blog_set.count()
        return 0

    def pub_blogs(self):
        return self.blog_set.filter(is_published=True)

    def arch_blogs(self):
        return self.blog_set.filter(is_published=False)

    def saved_blogs(self):
        return Blog.videoobjects.filter(saves__id=self.pk)

    def get_video(self):
        if self.video:
            return self.video.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''


# class Relation(models.Model):
#     from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.from_user} following {self.to_user}'
