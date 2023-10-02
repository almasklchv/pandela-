# from blogs.utils import get_summary
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from profiles.views import message
from .models import Blog, Comment, Playlist
from .serializers import BlogSerializer, BlogListSerializer, BlogDetailSerializer, CommentSerializer, CommentCreateUpdateSerializer, PlaylistSerializer, PlaylistListSerializer, PlaylistDetailSerializer
from .pagination import SmallSetPagination,MediumSetPagination,LargeSetPagination
from .mixins import MultipleFieldLookupMixin

from django.shortcuts import render,get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions



from django.db.models.query_utils import Q


#плейлистовая движуха
from django.views.generic.list import ListView


class CreateBlogAPI(views.APIView):
    def post(self, request, pk):
        blog = Blog(
            author=get_user_model().objects.get(pk=request.data.get("author")),
            title=request.data.get("title"),
            video=request.data.get("video"),
            description=request.data.get("dscription"),
            thumbnail=request.data.get("thumbnail"),
            is_published=request.data.get("is_published"),
            playlist_setting=request.data.get("playlist"),
        )
        blog.save()
        return Response(status=status.HTTP_200_OK)


class ManageBlogAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.videoobjects.all()
    lookup_field = "id"

    # def patch(self, request, *args, **kwargs):
    #     # if request.data["content"]:
    #     #     request.data["summary"] = get_summary(request.data.get("content"))
    #     return super().patch(request, *args, **kwargs)


class LikeBlogAPI(views.APIView):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        user = request.user.profile
        if user in blog.likes.all():
            blog.likes.remove(user)
            # message(
            #     f"{user.name} ({user.pk}) убрал лайк с видео '{blog.title}' ({blog.pk})"
            # )
        else:
            blog.likes.add(user)
            # message(
            #     f"{user.name} ({user.pk}) лайкнул видео '{blog.title}' ({blog.pk})"
            # )
        serializer = BlogDetailSerializer(blog)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SaveBlogAPI(views.APIView):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        user = request.user.profile
        if user in blog.saves.all():
            blog.saves.remove(user)
            # message(
            #     f"{user.name} ({user.id}) unsaved the blog '{blog.title}' ({blog.id})"
            # )
        else:
            blog.saves.add(user)
            # message(
            #     f"{user.name} ({user.pk}) сохранил видео '{blog.title}' ({blog.pk})"
            # )
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
    def get(self, request, pk): #THERE WEREN'T  PK ONLY POST_SLUG BUT I THINK SLUG WILL SUCK WITH RUSSIAN LUNGUAGE(CHECK WIKIPEDIA)
        post = get_object_or_404(Blog, id=pk)
        post.viewed()
        serializer = BlogDetailSerializer(post)
        return Response({'post': serializer.data}, status=status.HTTP_200_OK)


#надо как-то совместить поиск аккаунтов и видео в одну копилку
class BlogAdvancedSearchTermView(APIView):
    def get(self, request, search_term):
        matches = Blog.videoobjects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(author__name__icontains=search_term) |
            Q(author__username__icontains=search_term) |# i added it. mb terminal will be angry cause profiles is another app
            # Q(content__icontains=search_term) | #change!!
            Q(playlist__name__icontains=search_term)
        )

        paginator = MediumSetPagination()
        results = paginator.paginate_queryset(matches, request)
        serializer = BlogListSerializer(results, many=True)

        return Response({
            'matches': serializer.data
        }, status=status.HTTP_200_OK)


class CreateCommentAPIView(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data

        parameters: [slug, body]

    """

    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
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

    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        comments = Comment.objects.filter(parent=blog)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


# class DetailCommentAPIView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
#     """
#     get:
#         Returns the details of a comment instance. Searches comment using comment id and post slug in the url.
#
#     put:
#         Updates an existing comment. Returns updated comment data
#
#         parameters: [parent, author, body]
#
#     delete:
#         Delete an existing comment
#
#         parameters: [parent, author, body]
#     """
#
#     # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     queryset = Comment.objects.all()
#     lookup_fields = ["parent"] #["parent", "id"]
#     serializer_class = CommentCreateUpdateSerializer


class PlaylistDetailView(APIView):
    def get(self, request, pk): #THERE WEREN'T  PK ONLY POST_SLUG BUT I THINK SLUG WILL SUCK WITH RUSSIAN LUNGUAGE(CHECK WIKIPEDIA)
        playlist = get_object_or_404(Blog, id=pk)
        serializer = PlaylistDetailSerializer(playlist)
        return Response({'playlist': serializer.data}, status=status.HTTP_200_OK)

# class PlaylistDetailView(ListView):
#     queryset = Playlist.objects.all()
#     lookup_fields = ["id"]
#     # page_type = "分类目录归档"

    # def get_queryset_data(self, pk):
    #     playlist = get_object_or_404(Playlist, id=pk)
    #
    #     playlistname = playlist.name
    #     # self.playlistname = playlistname
    #     # playlistnames = list(
    #     #     map(lambda c: c.name, playlist.get_sub_playlists()))
    #     # blog_list = Blog.objects.filter(
    #     #     playlist__name__in=playlistname, status='p')
    #     return blog_list

    # def get_queryset_cache_key(self): #хуй знает что это
    #     slug = self.kwargs['playlist_name']
    #     playlist = get_object_or_404(Playlist, slug=slug)
    #     playlistname = playlist.name
    #     self.playlistname = playlistname
    #     cache_key = 'playlist_list_{playlistname}_{page}'.format(
    #         playlistname=playlistname, page=self.page_number)
    #     return cache_key
    #
    # def get_context_data(self, **kwargs): #хуй знает что это
    #
    #     playlistname = self.playlistname
    #     try:
    #         playlistname = playlistname.split('/')[-1]
    #     except BaseException:
    #         pass
    #     kwargs['page_type'] = PlaylistDetailView.page_type
    #     # kwargs['tag_name'] = playlistname
    #     return super(PlaylistDetailView, self).get_context_data(**kwargs)


class CreatePlaylistView(views.APIView):
    def post(self, request, pk):
        playlist = Playlist(
            author=get_user_model().objects.get(id=pk),
            name=request.data.get("name"),
            description=request.data.get("description"),
            videos=request.data.get("videos"),
            # thumbnail=request.data.get("thumbnail"),
        )
        playlist.save()
        return Response(status=status.HTTP_200_OK)


class UpdatePlaylistView(generics.UpdateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

class DeletePlaylistView(generics.DestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]


class PlaylistListView(APIView):
    def get(self, request, format=None):
        if Playlist.objects.all().exists():
            playlists = Playlist.objects.all()
            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(playlists, request)
            serializer = PlaylistListSerializer(results, many=True)

            return paginator.get_paginated_response({'playlists': serializer.data})

        else:
            return Response({'error': 'Плейлисты не найдены!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

