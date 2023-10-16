# from blogs.utils import get_summary
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from profiles.views import message
from .models import Blog, Comment, Playlist
from .serializers import EditBlogSerializer, BlogListSerializer, BlogDetailSerializer, CommentSerializer, \
    CommentCreateUpdateSerializer, PlaylistSerializer, PlaylistListSerializer, PlaylistDetailSerializer, BlogSerializer
from .pagination import SmallSetPagination,MediumSetPagination,LargeSetPagination
# from .mixins import MultipleFieldLookupMixin

from django.shortcuts import render,get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions

from rest_framework.generics import (
    # CreateAPIView,
    # DestroyAPIView,
    # ListAPIView,
    # UpdateAPIView,
    # RetrieveAPIView,
    # RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)


from django.db.models.query_utils import Q


#плейлистовая движуха
from django.views.generic.list import ListView


class CreateBlogAPI(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def post(self, request):
        blog = Blog(
            author=request.user.profile.data.get("author"),#changed
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
    serializer_class = EditBlogSerializer
    queryset = Blog.videoobjects.all()
    permission_classes = [IsAuthenticated]
    # lookup_field = "id"

    # def get_queryset(self, *args, **kwargs):
    #     id = self.request.query_params.get('id')
    #     queryset = Blog.videoobjects.filter(id=kwargs["pk"])
    #     return queryset

    # def patch(self, request, *args, **kwargs):
    #     # if request.data["content"]:
    #     #     request.data["summary"] = get_summary(request.data.get("content"))
    #     return super().patch(request, *args, **kwargs)

    # def get(self, request): в профиле  есть. может пригодиться или надо будет из профиля убрать
    #     srz = self.serializer(instance=request.user.profile)

        # return Response(srz.data, status=status.HTTP_200_OK)
    def post(self, request, pk):
        srz = self.serializer_class(data=request.POST)
        blog = Blog.videoobjects.get(id=pk)
        if srz.is_valid():
            # blog.author = request.user.profile(это то что я добавлю если выяснится что аккаунт сможет сам выстава=лять  кто автор. вмес те с тем что уже есть)
            blog.author = srz.data['author']
            blog.title = srz.data['title']
            blog.description = srz.data['description']
            blog.thumbnail = srz.data['thumbnail']
            blog.video = srz.data['video']
            blog.is_published = srz.data['is_published']
            blog.playlist_setting = srz.data['playlist_setting']
            blog.save()

            Response(srz.data, status=status.HTTP_200_OK)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeBlogAPI(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self, request, pk):
        blog = Blog.videoobjects.get(id=pk)
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
        serializer = BlogSerializer(blog)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SaveBlogAPI(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self, request, pk):
        blog = Blog.videoobjects.get(id=pk)
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
        serializer = BlogSerializer(blog)
        return Response(status=status.HTTP_200_OK, data=serializer.data)




class BlogListView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    def get(self, request, format=None):
        if Blog.videoobjects.all().exists():
            blogs = Blog.videoobjects.all()
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(blogs, request)
            serializer = BlogListSerializer(results, many=True)

            return paginator.get_paginated_response({'blogs': serializer.data})

        else:
            return Response({'error': 'Posts not found!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PostDetailView(views.APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    def get(self, request, pk):
        blog = Blog.videoobjects.get(id=pk)
        blog.viewed()#хиты добавить после всмех багов
        # user = request.user.profile
        # if user in blog.saves.all():
        #     blog.saves.remove(user)
            # message(
            #     f"{user.name} ({user.id}) unsaved the blog '{blog.title}' ({blog.id})"
            # )
        # else:
        #     blog.saves.add(user)
            # message(
            #     f"{user.name} ({user.pk}) сохранил видео '{blog.title}' ({blog.pk})"
            # )
        serializer = BlogDetailSerializer(blog)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

# class PostDetailView(APIView):
#
#
#     # """
#     #     get:
#     #         Returns the details of a post instance. Searches post using slug field.
#     #
#     #     put:
#     #         Updates an existing post. Returns updated post data
#     #
#     #         parameters: [slug, title, body, description, image]
#     #
#     #     delete:
#     #         Delete an existing post
#     #
#     #         parameters = [slug]
#     #     """
#     # queryset = Blog.videoobjects.all()
#     # lookup_field = "id"
#     # serializer_class = BlogDetailSerializer
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#
#     # def get_object(self, *args, **kwargs):
#     #     # pk = self.kwargs.get('pk')
#     #     queryset = self.filter_queryset(self.get_queryset())
#     #     # make sure to catch 404's below
#     #     obj = queryset.get(kwargs={"id": self.object.pk})
#     #     # obj.viewed()
#     #     self.check_object_permissions(self.request, obj)
#     #     return obj
#
#     def get(self, request, pk): #THERE WEREN'T  PK ONLY POST_SLUG BUT I THINK SLUG WILL SUCK WITH RUSSIAN LUNGUAGE(CHECK WIKIPEDIA)
#         post = get_object_or_404(Blog, id=pk)
#         post.viewed()
#         serializer = BlogDetailSerializer(post)
#         return Response({'post': serializer.data}, status=status.HTTP_200_OK)


#надо как-то совместить поиск аккаунтов и видео в одну копилку
class BlogAdvancedSearchTermView(APIView):
    def get(self, request, search_term):
        matches = Blog.videoobjects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(author__name__icontains=search_term) |
            Q(author__username__icontains=search_term) |# i added it. mb terminal will be angry cause profiles is another app
            # Q(content__icontains=search_term) | #changed!!
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

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        blog = Blog.videoobjects.get(id=pk)
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


class PlaylistDetailView(views.APIView):
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly,
    # ]
    def get(self, request, pk): #THERE WEREN'T  PK ONLY POST_SLUG BUT I THINK SLUG WILL SUCK WITH RUSSIAN LUNGUAGE(CHECK WIKIPEDIA)
        # playlist = get_object_or_404(Blog, id=pk)
        playlist = Playlist.objects.get(id=pk)
        serializer = PlaylistDetailSerializer(playlist)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

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
    # def get_context_data(self, **kwargs): #это дополнительные штуки от жесткого чела контекстные модные крутые
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
    permission_classes = [IsAuthenticated]
    def post(self, request):
        playlist = Playlist(
            author=request.user.profile.data.get("author"),
            name=request.data.get("name"),
            description=request.data.get("description"),
            videos=request.data.get("videos"),
            thumbnail=request.data.get("thumbnail"),
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
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    def get(self, request, format=None):
        if Playlist.objects.all().exists():
            playlists = Playlist.objects.all()
            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(playlists, request)
            serializer = PlaylistListSerializer(results, many=True)

            return paginator.get_paginated_response({'playlists': serializer.data})

        else:
            return Response({'error': 'Плейлисты не найдены!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

