from django.http import Http404
from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    get_object_or_404,
)
from rest_framework.views import APIView
from .models import Date, Task
from .serializers import DateSerializer, TaskSerializer


class TaskCreateAPIView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        request_data = request.data
        try:
            day = request_data.pop('day', '')
            month = request_data.pop('month', '')
            year = request_data.pop('year', '')
            date, created = Date.objects.get_or_create(
                day=day,
                month=month,
                year=year,
                user=request.user
            )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request_data['date'] = date.pk
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskListAPIView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        day = request.data.pop('day', '')
        month = request.data.pop('month', '')
        year = request.data.pop('year', '')
        tasks = Task.objects.filter(date__user=request.user, date__day=day, date__month=month, date__year=year)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskUpdadeAPIView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        pk = request.data.pop('id', None)
        if pk is not None:
            task = get_object_or_404(Task, pk=pk, date__user__pk=request.user.pk)
            serializer = self.serializer_class(
                task, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class TaskDeleteAPIView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        pk = request.data.pop('id', None)
        task = get_object_or_404(Task, pk=pk, date__user__id=request.user.pk)
        task.delete()
        return Response(status=status.HTTP_200_OK)