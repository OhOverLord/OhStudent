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
from account.models import User
from .serializers import LectureSerializer


class LectureCreateAPIView(APIView):
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        request_data = request.data
        print(request.user.pk)
        request_data['user'] = request.user.pk
        serializer = self.serializer_class(data=request_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        return Lecture.objects.filter(user__pk=self.request.user.pk)