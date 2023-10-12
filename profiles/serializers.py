from rest_framework import serializers
from django.contrib.auth import get_user_model

from blogs.serializers import BlogSerializer


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ["name", "email", "username", "password"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class EmailUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "username"]


class PkProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id"]


class MiniProfileSerializer(serializers.ModelSerializer):
    followers = PkProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "username", "dp", "followers"]


class FollowProfileSerializer(serializers.ModelSerializer):
    followers = MiniProfileSerializer(many=True)
    following = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "followers", "following"]


class SearchProfileSerializer(serializers.ModelSerializer):
    followers = MiniProfileSerializer(many=True)
    no_of_blogs = BlogSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "username", "dp", "no_of_blogs", "no_of_followers", "followers", "bio"]


class ProfileSerializer(serializers.ModelSerializer):
    pub_blogs = BlogSerializer(many=True)
    arch_blogs = BlogSerializer(many=True)
    saved_blogs = BlogSerializer(many=True)
    # no_of_blogs = BlogSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    following = MiniProfileSerializer(many=True)


    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "name",
            "username",
            "email",
            "bio",
            "dp",
            "is_superuser",
            "followers",
            "following",
            "pub_blogs",
            "arch_blogs",
            "saved_blogs",
            "shapka",
            "main_name",
            "main_link",
            "second_name",
            "second_link",
            "third_name",
            "third_link",
            "fourth_name",
            "fourth_link",
            "fifth_name",
            "fifth_link",
            "no_of_blogs",
            "no_of_followers",
        ]

class ProfileDetailSerializer(serializers.ModelSerializer):
    pub_blogs = BlogSerializer(many=True)
    # arch_blogs = BlogSerializer(many=True)
    # saved_blogs = BlogSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    # following = MiniProfileSerializer(many=True)
    no_of_blogs = BlogSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "name",
            "username",
            "email",
            "bio",
            "dp",
            "shapka",
            "followers",
            # "following",
            "pub_blogs",
            # "arch_blogs",
            # "saved_blogs",
            # "main_name",
            "main_link",
            # "second_name",
            # "second_link",
            # "third_name",
            # "third_link",
            # "fourth_name",
            # "fourth_link",
            # "fifth_name",
            # "fifth_link",
            "no_of_blogs",
            "no_of_followers",
        ]

class ProfileInfoSerializer(serializers.ModelSerializer):
    pub_blogs = BlogSerializer(many=True)
            # arch_blogs = BlogSerializer(many=True)
            # saved_blogs = BlogSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    no_of_blogs = BlogSerializer(many=True)

            # following = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
                    "id",
                    "name",
                    "username",
                    "email",
                    "bio",
                    "dp",
                    "shapka",
                    "followers",
                    # "following",
                    # "pub_blogs",
                    # "arch_blogs",
                    # "saved_blogs",
                    "main_name",
                    "main_link",
                    "second_name",
                    "second_link",
                    "third_name",
                    "third_link",
                    "fourth_name",
                    "fourth_link",
                    "fifth_name",
                    "fifth_link",
                    "no_of_blogs",
                    "no_of_followers",
        ]


class AccountDetailSerializer(serializers.ModelSerializer):
    pub_blogs = BlogSerializer(many=True)
    # arch_blogs = BlogSerializer(many=True)
    # saved_blogs = BlogSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    # following = MiniProfileSerializer(many=True)
    no_of_blogs = BlogSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            # "id",
            "name",
            "username",
            "email",
            "bio",
            "dp",
            "shapka",
            "followers",
            # "following",
            "pub_blogs",
            # "arch_blogs",
            "saved_blogs",
            # "main_name",
            "main_link",
            # "second_name",
            # "second_link",
            # "third_name",
            # "third_link",
            # "fourth_name",
            # "fourth_link",
            # "fifth_name",
            # "fifth_link",
            "no_of_blogs",
            "no_of_followers",
        ]

class AccountArchiveSerializer(serializers.ModelSerializer):
    pub_blogs = BlogSerializer(many=True)
    arch_blogs = BlogSerializer(many=True)
    saved_blogs = BlogSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    # following = MiniProfileSerializer(many=True)
    no_of_blogs = BlogSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            # "id",
            "name",
            "username",
            "email",
            "bio",
            "dp",
            "shapka",
            "followers",
            # "following",
            # "pub_blogs",
            "arch_blogs",
            # "saved_blogs",
            # "main_name",
            "main_link",
            # "second_name",
            # "second_link",
            # "third_name",
            # "third_link",
            # "fourth_name",
            # "fourth_link",
            # "fifth_name",
            # "fifth_link",
            "no_of_blogs",
            "no_of_followers",
        ]

class AccountSavesSerializer(serializers.ModelSerializer):
    # pub_blogs = BlogSerializer(many=True)
    # arch_blogs = BlogSerializer(many=True)
    saved_blogs = BlogSerializer(many=True)
    # followers = MiniProfileSerializer(many=True)
    # following = MiniProfileSerializer(many=True)
    # no_of_blogs = BlogSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            # "id",
            # "name",
            # "username",
            # "email",
            # "bio",
            # "dp",
            # "shapka",
            # "followers",
            # "following",
            # "pub_blogs",
            # "arch_blogs",
            "saved_blogs",
            # "main_name",
            # "main_link",
            # "second_name",
            # "second_link",
            # "third_name",
            # "third_link",
            # "fourth_name",
            # "fourth_link",
            # "fifth_name",
            # "fifth_link",
            # "no_of_blogs",
        ]


class AccountFollowingSerializer(serializers.ModelSerializer):
    # pub_blogs = BlogSerializer(many=True)
    # arch_blogs = BlogSerializer(many=True)
    # saved_blogs = BlogSerializer(many=True)
    # followers = MiniProfileSerializer(many=True)
    following = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            # "id",
            # "name",
            # "username",
            # "email",
            # "bio",
            # "dp",
            # "shapka",
            # "followers",
            "following",
            # "pub_blogs",
            # "arch_blogs",
            # "saved_blogs",
            # "main_name",
            # "main_link",
            # "second_name",
            # "second_link",
            # "third_name",
            # "third_link",
            # "fourth_name",
            # "fourth_link",
            # "fifth_name",
            # "fifth_link",
            "no_of_following",
        ]

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "name",
            "username",
            "email",
            "bio",
            "dp",
            "shapka",
            "main_name",
            "main_link",
            "second_name",
            "second_link",
            "third_name",
            "third_link",
            "fourth_name",
            "fourth_link",
            "fifth_name",
            "fifth_link",
        )

# если эдит в get дает просто свой профиль, пусть там будут видны подписки и тд тп