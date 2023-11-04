from django.urls import path, re_path
from .views import *

from .elasticsearch_backend import ElasticSearchUserModelSearchForm
# from .views import EsUserSearchView
from haystack.views import search_view_factory


urlpatterns = [
    path("usernamesandemails/", UsernameAndEmails.as_view(), name="livecheck"),
    path("setup/<str:pk>/", SetupProfileAPI.as_view(), name="acc_setup"),
    # path("manage/<int:pk>/", ManageProfileAPI.as_view(), name="acc_manage"),
    path("delete/<str:pk>/", DeleteProfileAPI.as_view(), name="acc_delete"),
    path("searchhhh/", SearchProfileAPI.as_view(), name="acc_search"),
    path(
        "follow/<str:pk>/",
        FollowProfileAPI.as_view(),
        name="acc_follow",
    ),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    # path для отдельного профиля с пафом видео/плейлистов/о канале
    path('user/<str:pk>/', UserProfileView.as_view(), name='profile'),
    path('info/<str:pk>/', UserInfoView.as_view(), name='info-profile'),
    path('account/', UserAccountView.as_view(), name='account'),
    path('account/archive', AccountArchiveView.as_view(), name='archive'),
    path('saves/', AccountSavesView.as_view(), name='saves'),
    path('following/', AccountFollowingView.as_view(), name='following'),

    re_path('^search', search_view_factory(view_class=EsUserSearchView, form_class=ElasticSearchUserModelSearchForm),
            name='search'),

]
