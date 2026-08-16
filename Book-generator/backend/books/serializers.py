from rest_framework import serializers
from django.contrib.auth import get_user_model
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

User = get_user_model()


# ==============================================================================
# TAXONOMY & SERIES SERIALIZERS
# ==============================================================================

class SeriesSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(source='books.count', read_only=True)

    class Meta:
        model = Series
        fields = ['id', 'user', 'name', 'description', 'book_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


# ==============================================================================
# PROFILE & CREATIVE DIRECTION SERIALIZERS
# ==============================================================================

class BookProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookProfile
        fields = [
            'id', 'book', 'premise', 'logline', 'summary',
            'themes', 'central_conflict', 'ending_preference',
            'inspirations', 'must_include', 'must_avoid',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'book', 'created_at', 'updated_at']


# ==============================================================================
# WORLD BUILDING & LOCATION SERIALIZERS
# ==============================================================================

class LocationSerializer(serializers.ModelSerializer):
    importance_display = serializers.CharField(source='get_importance_display', read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'world', 'name', 'description', 'importance', 'importance_display', 'coordinates', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorldMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldMemory
        fields = ['id', 'world', 'key', 'value', 'importance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorldBuildingSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    memories = WorldMemorySerializer(many=True, read_only=True)

    class Meta:
        model = WorldBuilding
        fields = [
            'id', 'book', 'world_type', 'setting', 'era', 'time_period',
            'technology_level', 'magic_system', 'politics', 'religion',
            'economy', 'cultures', 'languages', 'world_rules', 'atmosphere',
            'notes', 'locations', 'memories', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'book', 'created_at', 'updated_at']


# ==============================================================================
# CHARACTER & RELATIONSHIP SERIALIZERS
# ==============================================================================

class CharacterMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterMemory
        fields = ['id', 'character', 'key', 'value', 'importance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CharacterRelationshipSerializer(serializers.ModelSerializer):
    character_from_name = serializers.CharField(source='character_from.name', read_only=True)
    character_to_name = serializers.CharField(source='character_to.name', read_only=True)
    relationship_type_display = serializers.CharField(source='get_relationship_type_display', read_only=True)

    class Meta:
        model = CharacterRelationship
        fields = [
            'id', 'character_from', 'character_from_name',
            'character_to', 'character_to_name',
            'relationship_type', 'relationship_type_display',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CharacterSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    memories = CharacterMemorySerializer(many=True, read_only=True)
    relationships_from = CharacterRelationshipSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = [
            'id', 'book', 'name', 'role', 'role_display', 'age', 'gender',
            'personality', 'appearance', 'background', 'goal', 'fear',
            'strengths', 'weaknesses', 'internal_conflict', 'external_conflict',
            'speech_style', 'habits', 'secrets', 'character_arc', 'notes',
            'memories', 'relationships_from', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==============================================================================
# STRUCTURE, CHAPTER, PLOT POINT & TIMELINE SERIALIZERS
# ==============================================================================

class RevisionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionHistory
        fields = ['id', 'chapter', 'old_text', 'new_text', 'reason', 'timestamp']
        read_only_fields = ['id', 'chapter', 'timestamp']


class ChapterSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    revisions = RevisionHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'book', 'chapter_number', 'generation_order', 'title',
            'summary', 'outline', 'generated_content', 'status', 'status_display',
            'estimated_words', 'actual_words', 'notes', 'revisions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StoryStructureSerializer(serializers.ModelSerializer):
    story_structure_display = serializers.CharField(source='get_story_structure_display', read_only=True)
    generation_strategy_display = serializers.CharField(source='get_generation_strategy_display', read_only=True)

    class Meta:
        model = StoryStructure
        fields = [
            'id', 'book', 'story_structure', 'story_structure_display',
            'chapter_count', 'chapter_length', 'outline_approved',
            'generation_mode', 'generation_strategy', 'generation_strategy_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'book', 'created_at', 'updated_at']


class PlotPointSerializer(serializers.ModelSerializer):
    importance_display = serializers.CharField(source='get_importance_display', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True, allow_null=True)

    class Meta:
        model = PlotPoint
        fields = [
            'id', 'book', 'chapter', 'chapter_title', 'title',
            'description', 'importance', 'importance_display',
            'resolved', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TimelineEventSerializer(serializers.ModelSerializer):
    chapter_title = serializers.CharField(source='chapter.title', read_only=True, allow_null=True)

    class Meta:
        model = TimelineEvent
        fields = [
            'id', 'book', 'chapter', 'chapter_title', 'title',
            'description', 'date', 'sequence', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==============================================================================
# AI CONFIGURATION SERIALIZERS
# ==============================================================================

class AIWritingStyleSerializer(serializers.ModelSerializer):
    pov_display = serializers.CharField(source='get_pov_display', read_only=True)
    tense_display = serializers.CharField(source='get_tense_display', read_only=True)

    class Meta:
        model = AIWritingStyle
        fields = [
            'id', 'book', 'pov', 'pov_display', 'tense', 'tense_display',
            'tone', 'writing_style', 'dialogue_level', 'description_level',
            'pacing', 'reading_level', 'vocabulary', 'violence_level',
            'romance_level', 'custom_instructions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'book', 'created_at', 'updated_at']


class AIGenerationSettingsSerializer(serializers.ModelSerializer):
    generation_mode_display = serializers.CharField(source='get_generation_mode_display', read_only=True)

    class Meta:
        model = AIGenerationSettings
        fields = [
            'id', 'book', 'generation_mode', 'generation_mode_display',
            'creativity', 'strictness', 'temperature', 'chapter_word_target',
            'generate_summaries_first', 'auto_approve', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'book', 'created_at', 'updated_at']


# ==============================================================================
# MEMORY SERIALIZERS
# ==============================================================================

class TimelineMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineMemory
        fields = ['id', 'book', 'key', 'value', 'importance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoreMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoreMemory
        fields = ['id', 'book', 'key', 'value', 'importance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==============================================================================
# ASSET & EXPORT SERIALIZERS
# ==============================================================================

class UploadedAssetSerializer(serializers.ModelSerializer):
    asset_type_display = serializers.CharField(source='get_asset_type_display', read_only=True)

    class Meta:
        model = UploadedAsset
        fields = [
            'id', 'book', 'title', 'asset_type', 'asset_type_display',
            'file', 'description', 'file_size', 'uploaded_at'
        ]
        read_only_fields = ['id', 'file_size', 'uploaded_at']


class ExportHistorySerializer(serializers.ModelSerializer):
    format_display = serializers.CharField(source='get_format_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ExportHistory
        fields = [
            'id', 'book', 'format', 'format_display', 'status',
            'status_display', 'file', 'error_message', 'export_date'
        ]
        read_only_fields = ['id', 'status', 'file', 'error_message', 'export_date']


# ==============================================================================
# BOOK SERIALIZERS (CREATE, LIST, DETAIL)
# ==============================================================================

class BookListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    book_type_display = serializers.CharField(source='get_book_type_display', read_only=True)
    chapter_count = serializers.IntegerField(source='chapters.count', read_only=True)
    series_name = serializers.CharField(source='series.name', read_only=True, allow_null=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'subtitle', 'slug', 'status', 'status_display',
            'book_type', 'book_type_display', 'genre', 'subgenre',
            'series', 'series_name', 'series_order', 'estimated_word_count',
            'actual_word_count', 'chapter_count', 'created_at', 'updated_at'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    book_type_display = serializers.CharField(source='get_book_type_display', read_only=True)
    series_name = serializers.CharField(source='series.name', read_only=True, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    profile = BookProfileSerializer(read_only=True)
    world_building = WorldBuildingSerializer(read_only=True)
    story_structure = StoryStructureSerializer(read_only=True)
    writing_style = AIWritingStyleSerializer(read_only=True)
    generation_settings = AIGenerationSettingsSerializer(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    plot_points = PlotPointSerializer(many=True, read_only=True)
    timeline_events = TimelineEventSerializer(many=True, read_only=True)
    assets = UploadedAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'user', 'series', 'series_name', 'series_order',
            'title', 'subtitle', 'slug', 'description', 'language',
            'status', 'status_display', 'book_type', 'book_type_display',
            'genre', 'subgenre', 'target_audience', 'reading_level',
            'estimated_word_count', 'actual_word_count', 'tags',
            'profile', 'world_building', 'story_structure',
            'writing_style', 'generation_settings', 'chapters',
            'characters', 'plot_points', 'timeline_events', 'assets',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class BookCreateSerializer(serializers.ModelSerializer):
    premise = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'subtitle', 'book_type', 'genre', 'subgenre',
            'target_audience', 'reading_level', 'estimated_word_count',
            'language', 'series', 'series_order', 'premise'
        ]

    def create(self, validated_data):
        premise = validated_data.pop('premise', '')
        user = self.context['request'].user if 'request' in self.context and self.context['request'].user.is_authenticated else None
        
        # Ensure fallback slug if not provided
        if 'slug' not in validated_data and 'title' in validated_data:
            from django.utils.text import slugify
            validated_data['slug'] = slugify(validated_data['title']) or 'untitled-book'

        book = Book.objects.create(user=user, **validated_data)

        # Automatically create related sub-models for clean initialization
        BookProfile.objects.create(book=book, premise=premise)
        StoryStructure.objects.create(book=book)
        AIWritingStyle.objects.create(book=book)
        AIGenerationSettings.objects.create(book=book)
        
        if book.book_type == 'fiction':
            WorldBuilding.objects.create(book=book)

        return book
