from .models import Course, Video
from django.db.models import Q



def searchCourses(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    videos = Video.objects.filter(title__icontains=search_query)

    courses = Course.objects.order_by('-created').distinct().filter(Q(title__icontains=search_query) |
                                   Q(description__icontains=search_query))

    return courses, search_query