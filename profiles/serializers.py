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
        fields = ["pk"]


class MiniProfileSerializer(serializers.ModelSerializer):
    followers = PkProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["pk", "name", "username", "dp", "followers"]


class FollowProfileSerializer(serializers.ModelSerializer):
    followers = MiniProfileSerializer(many=True)
    following = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["pk", "followers", "following"]


class SearchProfileSerializer(serializers.ModelSerializer):
    followers = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["pk", "name", "username", "dp", "followers"]


class ProfileSerializer(serializers.ModelSerializer):
    pub_blogs = BlogSerializer(many=True)
    arch_blogs = BlogSerializer(many=True)
    saved_blogs = BlogSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    following = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            "pk",
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
        ]
