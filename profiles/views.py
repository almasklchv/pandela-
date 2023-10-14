from django.contrib.auth.decorators import login_required
from rest_framework import generics, serializers, views, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from .models import Profile
from django.shortcuts import get_object_or_404
# from hitcount.models import HitCount
# from hitcount.views import HitCountMixin

# # Email sending and auth requirements
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage

# dev tools
from colorama import Fore, Style
import smtplib

from rest_framework.views import APIView

# local
from .serializers import *


def message(msg):
    print(Fore.MAGENTA, Style.BRIGHT, "\b\b[#]", Fore.RED, msg, Style.RESET_ALL)


class UsernameAndEmails(views.APIView):
    def get(self, request, pk):
        serializer = EmailUsernameSerializer(get_user_model().objects.all(), many=True)
        return Response(status=200, data=serializer.data)


class SetupProfileAPI(views.APIView):
    def post(self, request, pk):
        user = get_user_model().objects.get(id=pk)
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


# class ManageProfileAPI(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer
#     queryset = get_user_model().objects.all()
#     lookup_field = "pk"

class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = ProfileEditSerializer

    #по идее, если все правильно получилось, get - получить свой профиль. post - редактирование
    def get(self, request):
        srz = self.serializer(instance=request.user.profile)

        return Response(srz.data, status=status.HTTP_200_OK)

    def post(self, request):
        srz = self.serializer(data=request.POST)
        prof = get_user_model().objects.get(user=request.user)
        if srz.is_valid():
            prof.name = srz.data['name']
            prof.username = srz.data['username']
            prof.email = srz.data['email']
            prof.bio = srz.data['bio']
            prof.dp = srz.data['dp']
            prof.save()

            Response(srz.data, status=status.HTTP_200_OK)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserProfileView(APIView):
#     serializer_pro = ProfileSerializer
#
#     def get(self, request, *args, **kwargs):
#         # is_followig = False
#         user = get_user_model().objects.get(pk=kwargs["pk"])
#         srz = self.serializer_pro(instance=user)
#
#         srz_data = srz.data
#
#         return Response(srz_data, status=status.HTTP_200_OK)
#
#     def post(self, request, id):
#         form = self.form_class(request.POST)


class DeleteProfileAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        email = get_user_model().objects.get(id=pk).email
        password = request.data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is not None:
            message(f"{user.name} Удалил аккаунт :(")
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class FollowProfileAPI(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user.profile
        profile = get_user_model().objects.get(id=pk)
        if user in profile.followers.all():
            profile.followers.remove(user)
            user.following.remove(profile)
            message(f"{user.name}  unfollowed {profile.name} ")
        else:
            profile.followers.add(user)
            user.following.add(profile)
            message(f"{user.name} followed {profile.name} ")
        serializer = FollowProfileSerializer(profile)
        return Response(status=status.HTTP_200_OK, data=serializer.data)



class SearchProfileAPI(views.APIView):
    def post(self, request, pk):
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


class UserProfileView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    serializer_pro = ProfileDetailSerializer
    def get(self, request, pk):
        profile = get_user_model().objects.get(id=pk)
        # serializer = ProfileDetailSerializer(user)
        srz = self.serializer_pro(instance=profile)
        # data_list = [serializer.data, []]

        # relation = Relation.objects.filter(from_user=request.user, to_user=user)
        # if relation.exists():
        #     is_followig = True

        # srz_data = srz.data
        # srz_data['is_following'] = is_followig

        return Response(srz.data, status=status.HTTP_200_OK)

    # def post(self, request, pk): WTF IS THIS??
    #     form = self.form_class(request.POST)


# class UserProfileView(APIView): #APIView,HitCountMixin
#
#     def get(self, request, profileName, format=None):
#         self.object = get_object_or_404(Profile, username=profileName)
#         # hit_count = HitCount.objects.get_for_object(self.object)
#         # hit_count = self.hit_count(request, hit_count)
#         serializer = ProfileSerializer(self.object)
#         return Response(serializer.data)

# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_pro = ProfileDetailSerializer
#
#     def get(self, request, pk):
#         # is_followig = False
#         user = get_user_model().objects.get(id=pk)
#         srz = self.serializer_pro(instance=user)
#
#         # relation = Relation.objects.filter(from_user=request.user, to_user=user)
#         # if relation.exists():
#         #     is_followig = True
#
#         srz_data = srz.data
#         # srz_data['is_following'] = is_followig
#
#         return Response(srz_data, status=status.HTTP_200_OK)

class UserAccountView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # is_followig = False
        user = request.user.profile
        # srz = self.serializer_pro(instance=user)
        serializer = AccountDetailSerializer(user)

        # relation = Relation.objects.filter(from_user=request.user, to_user=user)
        # if relation.exists():
        #     is_followig = True

        # srz_data = srz.data
        # srz_data['is_following'] = is_followig

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # def post(self, request, pk): WTF IS THIS??
    #     form = self.form_class(request.POST)


class UserInfoView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        # is_followig = False
        self.object = get_object_or_404(Profile, id=pk)
        # srz = self.serializer_pro(instance=user)
        serializer = ProfileInfoSerializer(self.object)

        # relation = Relation.objects.filter(from_user=request.user, to_user=user)
        # if relation.exists():
        #     is_followig = True

        # srz_data = srz.data
        # srz_data['is_following'] = is_followig

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class AccountSavesView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # is_followig = False
        user = request.user.profile
        serializer = AccountSavesSerializer(user)

        # relation = Relation.objects.filter(from_user=request.user, to_user=user)
        # if relation.exists():
        #     is_followig = True

        # srz_data = srz.data
        # srz_data['is_following'] = is_followig

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # def post(self, request, pk): WTF IS THIS??
    #     form = self.form_class(request.POST)

class AccountArchiveView(views.APIView):
    permission_classes = [IsAuthenticated]
    # serializer_pro = AccountArchiveSerializer

    def get(self, request):
            # is_followig = False
        user = request.user.profile
        serializer = AccountArchiveSerializer(user)

            # relation = Relation.objects.filter(from_user=request.user, to_user=user)
            # if relation.exists():
            #     is_followig = True

        # srz_data = srz.data
            # srz_data['is_following'] = is_followig

        return Response(status=status.HTTP_200_OK, data=serializer.data)

        # def post(self, request, pk): WTF IS THIS??
        #     form = self.form_class(request.POST)


class AccountFollowingView(views.APIView):
    permission_classes = [IsAuthenticated]
    # serializer_pro = AccountFollowingSerializer

    def get(self, request):
            # is_followig = False
        user = request.user.profile
        serializer = AccountFollowingSerializer(user)
        # srz = self.serializer_pro(instance=user)

            # relation = Relation.objects.filter(from_user=request.user, to_user=user)
            # if relation.exists():
            #     is_followig = True

        # srz_data = srz.data
            # srz_data['is_following'] = is_followig

        return Response(status=status.HTTP_200_OK, data=serializer.data)

        # def post(self, request, pk): WTF IS THIS??
        #     form = self.form_class(request.POST)