from django import template

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

import uuid

register = template.Library()
# Create your models here.

COURSE_TYPE=(
    ('программирование', 'Программирование'),
    ('дизайн', 'Дизайн'),
    ('маркетинг', 'Маркетинг')
)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Ваше Имя и Фамилия", max_length=200, blank=True, null=True, default="Ваш Аккаунт")
    username = models.CharField("Никнейм пользователя", max_length=50, blank=True, null=True)
    email = models.EmailField("Ваша электронная почта", max_length=300, blank=True, null=True)
    profile_image = models.ImageField("Фотография профиля", blank=True, null=True, upload_to='profiles/', default="profiles/account.png")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    teacher = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url


class Course(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=225)
    description = models.TextField("Описание", max_length=110)
    type = models.CharField("Выберите категорию", max_length=100, choices=COURSE_TYPE)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    preview = models.ImageField("Добавить заставку", upload_to='previews', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    @register.filter
    def order_by(queryset, args):
        args = [x.strip() for x in args.split(',')]
        return queryset.order_by(*args)

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('нравится', 'Нравится'),
        ('не нравится', 'Не Нравится'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'course']]

    def __str__(self):
        return self.value

class Video(models.Model):
    father = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=225, blank=True, null=True)
    file = models.FileField(upload_to='movies', blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title


