from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Blog, Comment


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["author", "title", "video", "description", "is_published"]


class MiniBProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["pk", "name", "username", "dp", "followers"] #can be mistake with adding followers


class BlogSerializer(serializers.ModelSerializer):
    likes = MiniBProfileSerializer(many=True)
    saves = MiniBProfileSerializer(many=True)
    author = MiniBProfileSerializer()
    thumbnail = serializers.CharField(source='get_thumbnail')
    video = serializers.CharField(source='get_video')
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = [
            "pk",
            "author",
            "title",
            "description",
            "thumbnail",
            "video",
            "likes",
            "no_of_likes",
            "saves",
            "views",
            "is_published",
            "comments",
        ]

class BlogListSerializer(serializers.ModelSerializer):
    # likes = MiniWriterSerializer(many=True)
    # saves = MiniWriterSerializer(many=True)
    author = MiniBProfileSerializer()
    thumbnail = serializers.CharField(source='get_thumbnail')
    # video = serializers.CharField(source='get_video')
    # comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = [
            "pk",
            "author",
            "title",
            # "description",
            "thumbnail",
            # "video",
            # "likes",
            # "no_of_likes",
            # "saves",
            "views",
            "is_published",
        ]

class BlogDetailSerializer(serializers.ModelSerializer):
        likes = MiniBProfileSerializer(many=True)
        saves = MiniBProfileSerializer(many=True)
        author = MiniBProfileSerializer()
        # thumbnail = serializers.CharField(source='get_thumbnail')
        video = serializers.CharField(source='get_video')
        comments = serializers.SerializerMethodField(read_only=True)

        class Meta:
            model = Blog
            fields = [
                "pk",
                "author",
                "title",
                "description",
                # "thumbnail",
                "video",
                "likes",
                "no_of_likes",
                "saves",
                "is_published",
                "comments",
                "views",
            ]

        def get_comments(self, obj):
            qs = Comment.objects.filter(parent=obj)
            return qs

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
            "created_at",
            "updated_at",
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "author",
            "parent",
            "body",
        ]