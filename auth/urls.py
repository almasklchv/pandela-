from django.urls import path

from .views import SignInView, SignOutView, SignUpView

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path("/token/", TokenObtainPairView.as_view(), name="auth_token"),
    # path("/token/refresh", TokenRefreshView.as_view(), name="refresh_token"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/<int:pk>/", SignOutView.as_view(), name="signout"),
    # path("verifyemail/", VerifyEmailView.as_view(), name="verify_email"),
]
