from django.urls import path
from .views import *

urlpatterns = [
    # path("feed/", FeedAPI.as_view(), name="feed"),
    path("create/", CreateBlogAPI.as_view(), name="blog_create"),
    path("manage/<int:pk>/", ManageBlogAPI.as_view(), name="blog_manage"),
    path(
        "like/<int:blog_pk>/<int:writer_pk>/", LikeBlogAPI.as_view(), name="blog_like"
    ),
    path(
        "save/<int:blog_pk>/<int:writer_pk>/", SaveBlogAPI.as_view(), name="blog_save"
    ),
    path('', BlogListView.as_view()),
    # path('category/<category_id>', BlogListCategoryView.as_view()),
    path('video/<int:blog_pk>/', PostDetailView.as_view()),
    path('search/<str:search_term>', BlogAdvancedSearchTermView.as_view()),
    path("<int:blog_pk>/comment/", ListCommentAPIView.as_view(), name="list_comment"),
    path(
        "<int:blog_pk>/comment/create/",
        CreateCommentAPIView.as_view(),
        name="create_comment",
    ),
    path(
        "<int:blog_pk>/comment/<int:id>/",
        DetailCommentAPIView.as_view(),
        name="comment_detail",
    ),
]
