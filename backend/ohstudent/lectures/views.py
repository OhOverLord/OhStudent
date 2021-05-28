from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    get_object_or_404,
)
from rest_framework.views import APIView

from .models import Lecture
from account.models import User
from .serializers import LectureSerializer


class LectureCreateAPIView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        request_data = request.data
        print(request.user.pk)
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
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, pk):
        lecture = get_object_or_404(Lecture, pk=pk, user__id=request.user.pk)
        serializer = self.serializer_class(
            lecture, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class LectureDeleteView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, pk):
        lecture = get_object_or_404(Lecture, pk=pk, user__id=request.user.pk)
        lecture.delete()
        return Response(status=status.HTTP_200_OK)


class LecuresListView(ListAPIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Lecture.objects.filter(user__pk=self.request.user.pk)