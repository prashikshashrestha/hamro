from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    Series,
    Tag,
    Book,
    BookProfile,
    WorldBuilding,
    Location,
    Character,
    CharacterRelationship,
    StoryStructure,
    Chapter,
    PlotPoint,
    TimelineEvent,
    AIWritingStyle,
    AIGenerationSettings,
    CharacterMemory,
    WorldMemory,
    TimelineMemory,
    LoreMemory,
    UploadedAsset,
    ExportHistory,
    RevisionHistory
)
from .serializers import (
    SeriesSerializer,
    TagSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookCreateSerializer,
    BookProfileSerializer,
    WorldBuildingSerializer,
    LocationSerializer,
    CharacterSerializer,
    CharacterRelationshipSerializer,
    StoryStructureSerializer,
    ChapterSerializer,
    PlotPointSerializer,
    TimelineEventSerializer,
    AIWritingStyleSerializer,
    AIGenerationSettingsSerializer,
    CharacterMemorySerializer,
    WorldMemorySerializer,
    TimelineMemorySerializer,
    LoreMemorySerializer,
    UploadedAssetSerializer,
    ExportHistorySerializer,
    RevisionHistorySerializer
)


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related(
        'series', 'profile', 'world_building', 'story_structure',
        'writing_style', 'generation_settings'
    ).prefetch_related('tags', 'chapters', 'characters', 'plot_points', 'timeline_events')

    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer
        elif self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

    @action(detail=True, methods=['post'], url_path='generate')
    def trigger_generation(self, request, pk=None):
        """Trigger AI generation pipeline for the book"""
        book = self.get_object()
        book.status = 'writing'
        book.save()
        
        # Generator pipeline service call can be wired here
        return Response({
            'id': book.id,
            'status': book.status,
            'message': 'Generation pipeline initiated successfully.'
        }, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'], url_path='summary')
    def full_summary(self, request, pk=None):
        """Returns consolidated high-level overview of book and creative assets"""
        book = self.get_object()
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filterset_fields = ['book', 'role']


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    filterset_fields = ['book', 'status']

    @action(detail=True, methods=['post'], url_path='revision')
    def request_revision(self, request, pk=None):
        """Log a revision request for a chapter"""
        chapter = self.get_object()
        reason = request.data.get('reason', 'User requested polish')
        new_text = request.data.get('new_text', chapter.generated_content)

        RevisionHistory.objects.create(
            chapter=chapter,
            old_text=chapter.generated_content,
            new_text=new_text,
            reason=reason
        )

        chapter.generated_content = new_text
        chapter.status = 'polishing'
        chapter.save()

        return Response(ChapterSerializer(chapter).data)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class PlotPointViewSet(viewsets.ModelViewSet):
    queryset = PlotPoint.objects.all()
    serializer_class = PlotPointSerializer
    filterset_fields = ['book', 'resolved', 'importance']


class TimelineEventViewSet(viewsets.ModelViewSet):
    queryset = TimelineEvent.objects.all().order_by('sequence')
    serializer_class = TimelineEventSerializer
    filterset_fields = ['book']


class UploadedAssetViewSet(viewsets.ModelViewSet):
    queryset = UploadedAsset.objects.all()
    serializer_class = UploadedAssetSerializer
    filterset_fields = ['book', 'asset_type']


class ExportHistoryViewSet(viewsets.ModelViewSet):
    queryset = ExportHistory.objects.all()
    serializer_class = ExportHistorySerializer
    filterset_fields = ['book', 'format', 'status']
