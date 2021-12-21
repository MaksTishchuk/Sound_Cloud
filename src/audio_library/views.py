import os

from django.http import FileResponse, Http404
from rest_framework import generics, viewsets, parsers, views
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers
from ..base.classes import MixedSerializer, Pagination
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file


class GenreView(generics.ListAPIView):
    """Список жанров"""

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """CRUD лицензий автора"""

    serializer_class = serializers.LicenseSerializer
    permission_classes = [IsAuthor, ]

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumView(viewsets.ModelViewSet):
    """CRUD для альбомов автора"""

    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = [IsAuthor, ]

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    """Список публичных альбомов автора"""

    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD треков"""

    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.CreateAuthorTrackSerializer
    permission_classes = [IsAuthor, ]
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer,
    }

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.file.path)
        delete_old_file(instance.cover.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD плейлистов"""

    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.CreatePlayListSerializer
    permission_classes = [IsAuthor, ]
    serializer_classes_by_action = {
        'list': serializers.PlayListSerializer,
    }

    def get_queryset(self):
        return models.PlayList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class TrackListView(generics.ListAPIView):
    """Список всех треков"""

    queryset = models.Track.objects.filter(album__private=False, private=False)
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']


class AuthorTrackListView(generics.ListAPIView):
    """Список всех треков конкретного автора"""

    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'album__name', 'genre__name']


    def get_queryset(self):
        return models.Track.objects.filter(
            user__id=self.kwargs.get('pk'),
            album__private=False,
            private=False
        )


class StreamingFileView(views.APIView):
    """Получение и проигрывание трека"""

    def set_play(self, track):
        track.plays_count += 1
        track.save()

    def get(self, request, pk):
        track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(track.file.path):
            self.set_play(track)
            return FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
        else:
            return Http404


class DownloadTrackView(views.APIView):
    """Скачивание трека"""

    def set_download(self):
        self.track.download_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(self.track.file.path):
            self.set_download()
            return FileResponse(
                open(self.track.file.path, 'rb'), filename=self.track.file.name, as_attachment=True
            )
        else:
            return Http404


class CommentAuthorView(viewsets.ModelViewSet):
    """CRUD комментариев автора"""

    serializer_class = serializers.CommentAuthorSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """Комментарии к треку"""

    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(track_id=self.kwargs.get('pk'))


