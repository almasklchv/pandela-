from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Blog, Comment, Playlist


# class CreateBlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blog
#         fields = ["author", "title", "video", "description", "is_published"]

# class CreateCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blog
#         fields = ["name", "parent_category",  "thumbnail"]


class MiniBProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "name", "username", "dp", "followers"] #can be mistake with adding followers


class BlogSerializer(serializers.ModelSerializer):
    likes = MiniBProfileSerializer(many=True)
    saves = MiniBProfileSerializer(many=True)
    author = MiniBProfileSerializer()
    thumbnail = serializers.CharField(source='get_thumbnail')
    video = serializers.CharField(source='get_video')
    comments = serializers.SerializerMethodField(read_only=True)
    views = MiniBProfileSerializer(many=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "author",
            "title",
            "description",
            "thumbnail",
            "video",
            "likes",
            # "no_of_likes",
            # "no_of_saves",
            "saves",
            "views",
            "is_published",
            "comments",
            "playlist_setting",
        ]

    def get_comments(self, obj):
        qs = Comment.objects.filter(parent=obj)
        return qs

class EditBlogSerializer(serializers.ModelSerializer):
    # likes = MiniBProfileSerializer(many=True)
    # saves = MiniBProfileSerializer(many=True)
    author = MiniBProfileSerializer()
    thumbnail = serializers.CharField(source='get_thumbnail')
    video = serializers.CharField(source='get_video')
    # comments = serializers.SerializerMethodField(read_only=True)
    # views = MiniBProfileSerializer(many=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "author",
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
            "playlist_setting",
        ]

    def get_comments(self, obj):
        qs = Comment.objects.filter(parent=obj)
        return qs

class BlogListSerializer(serializers.ModelSerializer):
    # likes = MiniWriterSerializer(many=True)
    # saves = MiniWriterSerializer(many=True)
    author = MiniBProfileSerializer()
    thumbnail = serializers.CharField(source='get_thumbnail')
    video = serializers.CharField(source='get_video')
    # views = MiniBProfileSerializer(many=True)
    #ADD NUMBER  OF VIEWS NOT VIEWS
    class Meta:
        model = Blog
        fields = [
            "id",
            "author",
            "title",
            "description",
            "thumbnail",
            "video",
            "no_of_saves",
            "no_of_likes",
            "pub_date",
            "views",
            "is_published",
        ]

class BlogDetailSerializer(serializers.ModelSerializer):
        # id = serializers.SerializerMethodField(read_only=True)
        # likes = MiniBProfileSerializer(many=True)
        # saves = MiniBProfileSerializer(many=True)
        # views = MiniBProfileSerializer(many=True)
        # thumbnail = serializers.CharField(source='get_thumbnail')
        video = serializers.CharField(source='get_video')
        # comments = serializers.SerializerMethodField(read_only=True)
        author = MiniBProfileSerializer()
        comments = serializers.SerializerMethodField('get_comments')

        class Meta:
            model = Blog
            fields = [
                "id",
                "author",
                "title",
                "description",
                # "thumbnail",
                "video",
                # "likes",
                "no_of_likes",
                "no_of_saves",
                # "saves",
                "is_published",
                "comments",
                "views",
                "playlist_setting",
                "pub_date",
            ]

        def get_id(self, obj):
            return obj.id
        def get_comments(self, obj):
            qs = Comment.objects.filter(parent=obj)
            serializer = CommentSerializer(qs, many=True)
            return serializer.data

# class DeleteWriterAPI(views.APIView):
#     def post(self, request, *args, **kwargs):
#         email = get_user_model().objects.get(pk=kwargs["pk"]).email
#         password = request.data.get("password", None)
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             message(f"{user.name} ({user.pk}) Удалил аккаунт :(")
#             user.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "parent",
            "author",
            "body",
            "pub_date",
            "mod_date",
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "author",
            "parent",
            "body",
        ]

class PlaylistSerializer(serializers.ModelSerializer):
    thumbnail = serializers.CharField(source='get_thumbnail')
    class Meta:
        model = Playlist
        fields = [
            "name",
            "author",
            "description",
            "mod_date",
            "videos",
            "pub_date",
            "thumbnail",
            "id",
        ]


class PlaylistDetailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.CharField(source='get_thumbnail')
    author = MiniBProfileSerializer()
    class Meta:
        model = Playlist
        fields = [
            "name",
            "author",
            "description",
            "mod_date",
            "videos",
            "pub_date",
            "thumbnail",
            "id",
        ]



class PlaylistListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.CharField(source='get_thumbnail')
    class Meta:
        model = Playlist
        fields = [
            "name",
            "description",
            "author",
            "pub_date",
            "thumbnail",
        ]