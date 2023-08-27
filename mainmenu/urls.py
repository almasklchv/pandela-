from django.urls import path
from . import views


urlpatterns = [
    path('', views.courses, name='courses'),
    path('course/<str:pk>/', views.course, name='course'),

    path('course_create/', views.createCourse, name='course_create'),
    path('update_course/<str:pk>/', views.updateCourse, name='update_course'),
    path('delete_course/<str:pk>/', views.deleteCourse, name='delete_course'),

    path('watch/<str:pk>/', views.watchVideo, name='watch_video'),

    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('account/', views.userAccount, name="account"),
    path('edit-account', views.editAccount, name="edit-account"),

    path('premium/', views.premiumPage, name="premium"),

]

# path for premium. you should name it "premium"
# page o nas. we don't have it