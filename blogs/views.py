# from blogs.utils import get_summary
from rest_framework import generics, views, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from profiles.views import message
from .models import Blog, Comment
from .serializers import BlogSerializer, BlogListSerializer, BlogDetailSerializer, CommentSerializer, CommentCreateUpdateSerializer
from .pagination import SmallSetPagination,MediumSetPagination,LargeSetPagination
from .mixins import MultipleFieldLookupMixin

from django.shortcuts import render,get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions



from django.db.models.query_utils import Q


class CreateBlogAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        blog = Blog(
            author=get_user_model().objects.get(pk=request.data.get("author")),
            title=request.data.get("title"),
            video=request.data.get("video"),
            description=request.data.get("dscription"),
            thumbnail=request.data.get("thumbnail"),
            is_published=request.data.get("is_published"),
        )
        blog.save()
        return Response(status=status.HTTP_200_OK)


class ManageBlogAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.videoobjects.all()
    lookup_field = "pk"

    # def patch(self, request, *args, **kwargs):
    #     # if request.data["content"]:
    #     #     request.data["summary"] = get_summary(request.data.get("content"))
    #     return super().patch(request, *args, **kwargs)


class LikeBlogAPI(views.APIView):
    def get(self, request, **kwargs):
        blog = Blog.objects.get(pk=kwargs["blog_pk"])
        user = get_user_model().objects.get(pk=kwargs["profile_pk"])
        if user in blog.likes.all():
            blog.likes.remove(user)
            message(
                f"{user.name} ({user.pk}) убрал лайк с видео '{blog.title}' ({blog.pk})"
            )
        else:
            blog.likes.add(user)
            message(
                f"{user.name} ({user.pk}) лайкнул видео '{blog.title}' ({blog.pk})"
            )
        serializer = BlogDetailSerializer(blog)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SaveBlogAPI(views.APIView):
    def get(self, request, **kwargs):
        blog = Blog.objects.get(pk=kwargs["blog_pk"])
        user = get_user_model().objects.get(pk=kwargs["profile_pk"])
        if user in blog.saves.all():
            blog.saves.remove(user)
            message(
                f"{user.name} ({user.pk}) unsaved the blog '{blog.title}' ({blog.pk})"
            )
        else:
            blog.saves.add(user)
            message(
                f"{user.name} ({user.pk}) сохранил видео '{blog.title}' ({blog.pk})"
            )
        serializer = BlogDetailSerializer(blog)
        return Response(status=status.HTTP_200_OK, data=serializer.data)




class BlogListView(APIView):
    def get(self, request, format=None):
        if Blog.videoobjects.all().exists():
            blogs = Blog.videoobjects.all()
            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(blogs, request)
            serializer = BlogListSerializer(results, many=True)

            return paginator.get_paginated_response({'blogs': serializer.data})

        else:
            return Response({'error': 'Posts not found!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailView(APIView):
    def get(self, request, format=None, **kwargs): #THERE WEREN'T  PK ONLY POST_SLUG BUT I THINK SLUG WILL SUCK WITH RUSSIAN LUNGUAGE(CHECK WIKIPEDIA)
        post = get_object_or_404(Blog, pk=kwargs["blog_pk"])
        post.viewed()
        serializer = BlogDetailSerializer(post)
        return Response({'post': serializer.data}, status=status.HTTP_200_OK)


#надо как-то совместить поиск аккаунтов и видео в одну копилку
class BlogAdvancedSearchTermView(APIView):
    def get(self, request, search_term):
        matches = Blog.videoobjects.filter(
            Q(title__icontains=search_term) |
            Q(content__icontains=search_term) | #change!!
            Q(category__name__icontains=search_term)
        )

        paginator = MediumSetPagination()
        # results=paginator.paginate_queryset(matches,request)
        serializer = BlogListSerializer(matches, many=True)

        return Response({
            'filtered_posts': serializer.data
        }, status=status.HTTP_200_OK)


class CreateCommentAPIView(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data

        parameters: [slug, body]

    """

    serializer_class = CommentCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs["blog_pk"])
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=blog) #author=user parent=video
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListCommentAPIView(APIView):
    """
    get:
        Returns the list of comments on a particular post
    """

    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, **kwargs):
        blog = Blog.objects.get(pk=kwargs["blog_pk"])
        comments = Comment.objects.filter(parent=blog)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class DetailCommentAPIView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a comment instance. Searches comment using comment id and post slug in the url.

    put:
        Updates an existing comment. Returns updated comment data

        parameters: [parent, author, body]

    delete:
        Delete an existing comment

        parameters: [parent, author, body]
    """

    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Comment.objects.all()
    lookup_fields = ["parent"] #["parent", "id"]
    serializer_class = CommentCreateUpdateSerializer