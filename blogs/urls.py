from django.urls import path
from .views import *

urlpatterns = [
    # path("feed/", FeedAPI.as_view(), name="feed"),
    path("create/", CreateBlogAPI.as_view(), name="blog_create"),
    path("manage/<str:pk>/", ManageBlogAPI.as_view(), name="blog_manage"),
    path(
        "like/<str:pk>/", LikeBlogAPI.as_view(), name="blog_like"
    ),
    path(
        "save/<str:pk>/", SaveBlogAPI.as_view(), name="blog_save"
    ),
    path('', BlogListView.as_view()),
    # path('category/<category_id>', BlogListCategoryView.as_view()),
    path('video/<str:pk>/', PostDetailView.as_view()),
    path('search/<str:search_term>', BlogAdvancedSearchTermView.as_view()),
    path("<str:blog_pk>/comment/", ListCommentAPIView.as_view(), name="list_comment"),
    path(
        "<str:pk>/comment/create/",
        CreateCommentAPIView.as_view(),
        name="create_comment",
    ),
    # path(
    #     "<str:blog_pk>/<str:writer_pk>/comment/<str:comment_pk>/",
    #     DetailCommentAPIView.as_view(),
    #     name="comment_detail",
    # ),

    path(
        'playlist/<str:pk>/',
        PlaylistDetailView.as_view(),
        name='playlist_detail'),
    path(
        'playlists/',
        PlaylistListView.as_view(),
        name='playlist_detail'),
    # path(
    #     'playlist/<str:pk>/<int:page>.html/',
    #     PlaylistDetailView.as_view(),
    #     name='playlist_detail_page'),
    #нужен паф страницы добавления удаления categories
    path('playlist/create/', CreatePlaylistView.as_view(), name='create-playlist'),
    path('playlist/update/<str:pk>/', UpdatePlaylistView.as_view(), name='update-playlist'),
    path('playlist/delete/<str:pk>/', DeletePlaylistView.as_view(), name='delete-playlist'),
]
