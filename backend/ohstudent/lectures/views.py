from builtins import print
from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    get_object_or_404,
)
from rest_framework.views import APIView

from .models import Folder, Lecture
from account.models import User
from .serializers import FolderSerializer, LectureSerializer, LectureDetailSerializer


class LectureCreateAPIView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        request_data = request.data
        request_data['user'] = request.user.pk
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LectureDetailView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk):
        lecture = get_object_or_404(Lecture, pk=pk, user__id=request.user.pk)
        serializer = self.serializer_class(lecture)
        return Response(serializer.data)


class LectureUpdateView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        pk = request.data.pop('id', None)
        if pk is not None:
            lecture = get_object_or_404(Lecture, pk=pk, user__id=request.user.pk)
            serializer = self.serializer_class(
                lecture, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)



class LectureDeleteView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        pk = request.data.pop('id', None)
        lecture = get_object_or_404(Lecture, pk=pk, user__id=request.user.pk)
        lecture.delete()
        return Response(status=status.HTTP_200_OK)


class LecuresListView(ListAPIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Lecture.objects.filter(user__pk=self.request.user.pk)

class LectureShareView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        pk = request.data.pop('id', None)
        lecture = get_object_or_404(Lecture, pk=pk, user__id=request.user.pk)
        lecture.status = "public"
        lecture.save()
        serializer = self.serializer_class(lecture)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PublicLectureDetailView(APIView):
    serializer_class = LectureDetailSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        pk = request.data.pop('id', None)
        lecture = get_object_or_404(Lecture, pk=pk, status="public")
        serializer = self.serializer_class(lecture)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FolderCreateAPIView(APIView):
    serializer_class = FolderSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        request_data = request.data
        request_data['user'] = request.user.pk
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FolderListAPIView(ListAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Folder.objects.filter(user__pk=self.request.user.pk)


class FolderUpdateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = FolderSerializer

    def update(self, request):
        pk = request.data.pop('id', None)
        if pk is not None:
            folder = get_object_or_404(Folder, pk=pk, user__id=request.user.pk)
            serializer = self.serializer_class(
                folder, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FolderDeleteAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = FolderSerializer

    def post(self, request):
        pk = request.data.pop('id', None)
        if pk is not None:
            folder = get_object_or_404(Folder, pk=pk, user__id=request.user.pk)
            folder.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
