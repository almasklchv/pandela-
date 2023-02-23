from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated #IsAdminUser - для админов
from rest_framework.response import Response
from .serializers import CourseSerializer
from mainmenu.models import Course



@api_view(['GET'])
@permission_classes([IsAuthenticated]) #нужно быть авторизованным, чтобы получить данные
def getRoutes(request):

    routes = [
        {'GET': '/api/courses'},
        {'GET': '/api/courses/id'},
        {'GET': '/api/courses/'},

        {'POST': '/api/courses/token'},
        {'POST': '/api/courses/token/refresh'},
    ]

    return Response(routes)


@api_view(['GET'])
def getCourses(request):
    print('USER:', request.user)
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCourse(request, pk):
    course = Course.objects.get(id=pk)
    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)