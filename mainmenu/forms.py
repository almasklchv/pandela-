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
            field.widget.attrs.update({'class': 'form__text-input'})
           # on a real  web page, you probably
           # don’t want every  widget  to look the same.You  might  want  a   larger   input  element   for the comment, and you might want the ‘name’ widget
          #  to have some special CSS class.It is also possible to specify the ‘type’ attribute to take advantage of the new HTML5 input types.To do this, you use the Widget.attrs argument when creating the widget:


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'email', 'profile_image']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for username, field in self.fields.items():
            field.widget.attrs.update({'class': 'form__text-input'})

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'type', 'preview']#нужно чтобы в формочке был плюсик чтобы добавлять сколько хочешь видео
        widgets = {
            # 'videos': forms.CheckboxSelectMultiple(),
            'type': forms.Select(attrs={'class': 'choose-category'}),
            'title': forms.TextInput(attrs={'class': 'form__text-input'}),
            'description': forms.TextInput(attrs={'class': 'form__text-input'}),
        }



class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__text-input'}),
        }




class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Поставьте оценку',
            'body': 'Добавьте комментарий  к оценке'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})