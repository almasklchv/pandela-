from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Course, Video, Review
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'email', 'profile_image']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'type', 'preview']#нужно чтобы в формочке был плюсик чтобы добавлять сколько хочешь видео
        widgets = {
            'videos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

        for title, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'file']

# VideoFormSet = modelformset_factory(
#     Video, fields=('title',  'file'), extra=1
# )



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})