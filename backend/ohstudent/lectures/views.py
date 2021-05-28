from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    get_object_or_404,
    RetrieveAPIView
)
from rest_framework.views import APIView

from .models import Lecture
from .serializers import LectureSerializer


class LectureCreateAPIView(CreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )


class LectureDetailView(RetrieveAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )


class LectureUpdateView(UpdateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

class LectureDeleteView(DestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )


class LecuresListView(ListAPIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        queryset = contact.chats.filter(participants__id=self.request.user.id)
        return queryset