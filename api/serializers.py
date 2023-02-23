from rest_framework import serializers
from mainmenu.models import Profile, Course

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    class Meta:
        model = Course
        fields = '__all__'