from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib. auth.models import User
from .models import Profile, Course, Review, Video
from .forms import CustomUserCreationForm, ProfileForm, CourseForm, VideoForm, ReviewForm
from django.views.decorators.csrf import csrf_protect
from .utils import searchCourses
from django.forms.models import modelformset_factory

# Create your views here.

def courses(request):
    courses, search_query = searchCourses(request)  # оптимизация кода. Перенос кода в utils

    context = {'courses': courses, 'search_query': search_query}
    return render(request, 'mainmenu/main.html', context)

def course(request, pk):
    courseObj = Course.objects.get(id=pk)
    form = ReviewForm()


    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.course = courseObj
        review.owner = request.user.profile
        review.save()

        courseObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('course', pk=courseObj.id)

    return render(request, 'mainmenu/course.html', {'course': courseObj, 'form': form})


def handle_not_found(request, exception):
    return render(request, '404.html')

@csrf_protect
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('courses')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Такого аккаунта не существует')

        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return redirect('courses')
        else:
            messages.error(request, 'Никнейм или пароль неверный')
    return render(request, 'mainmenu/login_registeration.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')

@csrf_protect
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)# Не хотим, чтобы аккаунты денисайви и Денисайви отличались между собой
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Аккаунт был создан!')

            login(request, user)
            return redirect('edit-account')
    else:
        messages.success(request, 'Произошла ошибка... Создать аккаунт не удаётся по неведомым причинам :(')

    context = {'page': page, 'form': form}
    return render(request, 'mainmenu/login_registeration.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    stories = profile.story_set.all()
    context = {'profile': profile, 'stories': stories}
    return render(request, 'mainmenu/profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    # courses = profile.story_set.all()
    context = {'profile': profile}
    return render(request, 'mainmenu/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form': form}
    return render(request, 'mainmenu/profile_form.html', context)

@login_required(login_url="login")
def createCourse(request):
    form = CourseForm()
    profile = request.user.profile

    # VideoFormset = modelformset_factory(Video, form=VideoForm, extra=0)
    # formset = VideoFormset(request.POST or None)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = profile
            course.save()
            return redirect('update_course', pk=course.id)

    context = {'form': form}
    return render(request, "mainmenu/course_form.html", context)

@login_required(login_url="login")
def updateCourse(request, pk):
    profile = request.user.profile
    course = profile.course_set.get(id=pk)
    form = CourseForm(instance=course)

    VideoFormset = modelformset_factory(Video, form=VideoForm, extra=0)
    queryset = Video.objects.filter(father=course)
    formset = VideoFormset(queryset=queryset)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES , instance=course)
        formset = VideoFormset(request.POST, request.FILES or None)
        if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)
            parent.save()
            for form in formset:
                child = form.save(commit=False)
                child.father = parent
                child.save()
                # parent.videos.add(child)
            # formset.owner = course
            # formset.save()
            # course.videos.add(formset)
            return redirect('courses')

    context = {'form': form, 'formset': formset, 'course': course}
    return render(request, "mainmenu/course_form.html", context)

@login_required(login_url="login")
def deleteCourse(request, pk):
    profile = request.user.profile
    course = profile.story_set.get(id=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('courses')
    context = {'object': course}
    return render(request, 'mainmenu/course_delete.html', context)


def watchVideo(request, pk):
    video = Video.objects.get(id=pk)
    context = {'video': video}
    return render(request, 'mainmenu/video_watch.html', context)