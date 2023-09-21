from rest_framework import generics, serializers, views, status
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q

# # Email sending and auth requirements
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage

# dev tools
from colorama import Fore, Style
import smtplib

# local
from .serializers import (
    ProfileSerializer,
    FollowProfileSerializer,
    EmailUsernameSerializer,
    SearchProfileSerializer,
)


def message(msg):
    print(Fore.MAGENTA, Style.BRIGHT, "\b\b[#]", Fore.RED, msg, Style.RESET_ALL)


class UsernameAndEmails(views.APIView):
    def get(self, request, **kwargs):
        serializer = EmailUsernameSerializer(get_user_model().objects.all(), many=True)
        return Response(status=200, data=serializer.data)


class SetupProfileAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=kwargs["pk"])
        try:
            check = get_user_model().objects.get(username=request.data.get("username"))
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            check = None
        if check is not None:
            return Response(
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                data={"error": "Такой никнейм уже используется"},
            )
        user.username = request.data.get("username")
        user.save()
        return Response(status=status.HTTP_200_OK)


class ManageProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = get_user_model().objects.all()
    lookup_field = "pk"


class DeleteProfileAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        email = get_user_model().objects.get(pk=kwargs["pk"]).email
        password = request.data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is not None:
            message(f"{user.name} ({user.pk}) Удалил аккаунт :(")
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class FollowProfileAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=kwargs["user_pk"])
        profile = get_user_model().objects.get(pk=kwargs["profile_pk"])
        if user in profile.followers.all():
            profile.followers.remove(user)
            user.following.remove(profile)
            message(f"{user.name} ({user.pk}) unfollowed {profile.name} ({profile.pk})")
        else:
            profile.followers.add(user)
            user.following.add(profile)
            message(f"{user.name} ({user.pk}) followed {profile.name} ({profile.pk})")
        serializer = FollowProfileSerializer(profile)
        return Response(status=status.HTTP_200_OK, data=serializer.data)



class SearchProfileAPI(views.APIView):
    def post(self, request, **kwargs):
        profile = request.data.get("username")
        bloggers = get_user_model().objects.filter(
            Q(username__contains=profile) | Q(name__contains=profile)
        )
        serializer = SearchProfileSerializer(bloggers, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def get(self, request, **kwargs):
        bloggers = get_user_model().objects.all()
        serializer = SearchProfileSerializer(bloggers, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
