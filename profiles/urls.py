from django.urls import path
from .views import *

urlpatterns = [
    path("usernamesandemails/", UsernameAndEmails.as_view(), name="livecheck"),
    path("setup/<int:pk>/", SetupProfileAPI.as_view(), name="acc_setup"),
    # path("manage/<int:pk>/", ManageProfileAPI.as_view(), name="acc_manage"),
    path("delete/<int:pk>/", DeleteProfileAPI.as_view(), name="acc_delete"),
    path("search/", SearchProfileAPI.as_view(), name="acc_search"),
    path(
        "follow/<int:user_pk>/<int:profile_pk>/",
        FollowProfileAPI.as_view(),
        name="acc_follow",
    ),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    # path для отдельного профиля с пафом видео/плейлистов/о канале
    path('profile/<int:id>', UserProfileView.as_view(), name='profile'),
    path('account/', UserAccountView.as_view(), name='account'),
]
