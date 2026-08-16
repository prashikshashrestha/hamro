from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SeriesViewSet,
    TagViewSet,
    BookViewSet,
    CharacterViewSet,
    ChapterViewSet,
    LocationViewSet,
    PlotPointViewSet,
    TimelineEventViewSet,
    UploadedAssetViewSet,
    ExportHistoryViewSet
)

router = DefaultRouter()
router.register(r'series', SeriesViewSet, basename='series')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'books', BookViewSet, basename='book')
router.register(r'characters', CharacterViewSet, basename='character')
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'plot-points', PlotPointViewSet, basename='plot-point')
router.register(r'timeline-events', TimelineEventViewSet, basename='timeline-event')
router.register(r'assets', UploadedAssetViewSet, basename='asset')
router.register(r'exports', ExportHistoryViewSet, basename='export')

urlpatterns = [
    path('', include(router.urls)),
]
