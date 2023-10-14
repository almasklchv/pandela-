from rest_framework import serializers
from django.contrib.auth import get_user_model

# from blogs.serializers import BlogSerializer
from blogs.models import Blog

class BlogPSerializer(serializers.ModelSerializer):
    # likes = MiniBProfileSerializer(many=True)
    # saves = MiniBProfileSerializer(many=True)
    # author = MiniBProfileSerializer()
    thumbnail = serializers.CharField(source='get_thumbnail')
    video = serializers.CharField(source='get_video')
    # comments = serializers.SerializerMethodField(read_only=True)
    # views = MiniBProfileSerializer(many=True)
    class Meta:
        model = Blog
        fields = [
            "id",
            # "author",
            "title",
            "description",
            "thumbnail",
            "video",
            # "likes",
            # "no_of_likes",
            # "no_of_saves",
            # "saves",
            # "views",
            "is_published",
            # "comments",
            # "playlist_setting",
        ]


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
        fields = ["id", "name", "username", "dp"]


class FollowProfileSerializer(serializers.ModelSerializer):
    followers = MiniProfileSerializer(many=True)
    following = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "followers", "following"]


class SearchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "name", "username", "dp",
                  "no_of_blogs", "no_of_followers",
                  "bio"]


class ProfileSerializer(serializers.ModelSerializer):
    pub_blogs = BlogPSerializer(many=True)
    arch_blogs = BlogPSerializer(many=True)
    saved_blogs = BlogPSerializer(many=True)
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
            "no_of_following",
        ]

class ProfileDetailSerializer(serializers.ModelSerializer):
    pub_blogs = BlogPSerializer(many=True)
    # arch_blogs = BlogSerializer(many=True)
    # # saved_blogs = BlogSerializer(many=True)
    # followers = MiniProfileSerializer(many=True)
    # following = MiniProfileSerializer(many=True)
    # no_of_blogs = BlogPSerializer(many=True)
    # posts = serializers.SerializerMethodField('get_user_posts')
    # posts = BlogPSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "name",
            "username",
            # "email",
            "bio",
            "dp",
            "shapka",
            # "followers",
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
            # "no_of_following",
            # "posts",
        ]

    # def get_posts(self, obj):
    #     result = obj.author_posts.all()
    #     return BlogSerializer(instance=result, many=True).data
    # def get_user_posts(self, author):
    #     post = Blog.videoobjects.filter(author=author.id)
    #     serializer = BlogPSerializer(post, many=True)
    #     return serializer.data

class ProfileInfoSerializer(serializers.ModelSerializer):
    # pub_blogs = BlogSerializer(many=True)
            # arch_blogs = BlogSerializer(many=True)
            # saved_blogs = BlogSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    # no_of_blogs = BlogSerializer(many=True)

            # following = MiniProfileSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
                    "id",
                    "name",
                    "username",
                    # "email",
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
                    # "no_of_no_of_following",
        ]


class AccountDetailSerializer(serializers.ModelSerializer):
    pub_blogs = BlogPSerializer(many=True)
    # arch_blogs = BlogSerializer(many=True)
    # saved_blogs = BlogSerializer(many=True)
    # followers = MiniProfileSerializer(many=True)
    # following = MiniProfileSerializer(many=True)
    # no_of_blogs = BlogPSerializer(many=True)

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
            # "followers",
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
            # "no_of_following",
        ]

class AccountArchiveSerializer(serializers.ModelSerializer):
    # pub_blogs = BlogPSerializer(many=True)
    arch_blogs = BlogPSerializer(many=True)
    # saved_blogs = BlogPSerializer(many=True)
    followers = MiniProfileSerializer(many=True)
    # following = MiniProfileSerializer(many=True)
    # no_of_blogs = BlogPSerializer(many=True)

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
            # "no_of_blogs",
            # "no_of_followers",
            "no_of_blogs",
            "no_of_followers",
            # "no_of_following",
        ]

class AccountSavesSerializer(serializers.ModelSerializer):
    # pub_blogs = BlogSerializer(many=True)
    # arch_blogs = BlogSerializer(many=True)
    saved_blogs = BlogPSerializer(many=True)
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
            # "no_of_following",
            # "no_of_blogs",
            # "no_of_followers",
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