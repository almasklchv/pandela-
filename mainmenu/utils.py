from .models import Course
from django.db.models import Q


def searchCourses(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')


    courses = Course.objects.distinct().filter(Q(title__icontains=search_query) |
                                                                    Q(description__icontains=search_query) |
                                                                    Q(type__icontains=search_query) |
                                               Q(owner__name__icontains=search_query) |
                                   Q(owner__username__icontains=search_query))

    return courses, search_query
