from django.contrib import admin
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


# ==============================================================================
# INLINE ADMIN MODELS
# ==============================================================================

class BookProfileInline(admin.StackedInline):
    model = BookProfile
    can_delete = False
    verbose_name_plural = "Creative Direction Profile"
    fk_name = 'book'
    extra = 0
    fieldsets = (
        ('Overview', {
            'fields': ('premise', 'logline', 'summary')
        }),
        ('Narrative Core', {
            'fields': ('themes', 'central_conflict', 'ending_preference')
        }),
        ('Directives & Rules', {
            'fields': ('inspirations', 'must_include', 'must_avoid')
        }),
    )


class StoryStructureInline(admin.StackedInline):
    model = StoryStructure
    can_delete = False
    verbose_name_plural = "Story Structure Setup"
    fk_name = 'book'
    extra = 0


class AIWritingStyleInline(admin.StackedInline):
    model = AIWritingStyle
    can_delete = False
    verbose_name_plural = "AI Writing Style Controls"
    fk_name = 'book'
    extra = 0
    fieldsets = (
        ('Voice & Perspective', {
            'fields': ('pov', 'tense', 'tone', 'writing_style')
        }),
        ('Detail & Pacing', {
            'fields': ('dialogue_level', 'description_level', 'pacing', 'reading_level', 'vocabulary')
        }),
        ('Content Boundaries', {
            'fields': ('violence_level', 'romance_level', 'custom_instructions')
        }),
    )


class AIGenerationSettingsInline(admin.StackedInline):
    model = AIGenerationSettings
    can_delete = False
    verbose_name_plural = "AI Generation Parameters"
    fk_name = 'book'
    extra = 0


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1
    fields = ('name', 'importance', 'description')


class WorldMemoryInline(admin.TabularInline):
    model = WorldMemory
    extra = 1
    fields = ('key', 'value', 'importance')


class CharacterMemoryInline(admin.TabularInline):
    model = CharacterMemory
    extra = 1
    fields = ('key', 'value', 'importance')


class CharacterRelationshipInline(admin.TabularInline):
    model = CharacterRelationship
    fk_name = 'character_from'
    extra = 1
    fields = ('character_to', 'relationship_type', 'description')


class RevisionHistoryInline(admin.TabularInline):
    model = RevisionHistory
    extra = 0
    readonly_fields = ('timestamp', 'reason', 'old_text', 'new_text')
    can_delete = False


# ==============================================================================
# MODEL ADMIN REGISTRATIONS
# ==============================================================================

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    list_filter = ('created_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'book_type', 'status', 'genre', 'estimated_word_count', 'actual_word_count', 'updated_at')
    list_filter = ('status', 'book_type', 'genre', 'language', 'created_at')
    search_fields = ('title', 'subtitle', 'slug', 'description', 'user__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    inlines = [BookProfileInline, StoryStructureInline, AIWritingStyleInline, AIGenerationSettingsInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'subtitle', 'slug', 'series', 'series_order', 'description', 'tags')
        }),
        ('Classification & Audience', {
            'fields': ('book_type', 'genre', 'subgenre', 'target_audience', 'reading_level', 'language')
        }),
        ('Status & Word Counts', {
            'fields': ('status', 'estimated_word_count', 'actual_word_count')
        }),
    )


@admin.register(BookProfile)
class BookProfileAdmin(admin.ModelAdmin):
    list_display = ('book', 'premise', 'logline', 'updated_at')
    search_fields = ('book__title', 'premise', 'logline', 'themes')


@admin.register(WorldBuilding)
class WorldBuildingAdmin(admin.ModelAdmin):
    list_display = ('book', 'world_type', 'era', 'technology_level', 'updated_at')
    search_fields = ('book__title', 'world_type', 'setting', 'magic_system')
    inlines = [LocationInline, WorldMemoryInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'world', 'importance', 'created_at')
    list_filter = ('importance',)
    search_fields = ('name', 'description', 'world__book__title')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'book', 'role', 'age', 'gender', 'updated_at')
    list_filter = ('role', 'gender')
    search_fields = ('name', 'personality', 'background', 'book__title')
    inlines = [CharacterMemoryInline, CharacterRelationshipInline]


@admin.register(CharacterRelationship)
class CharacterRelationshipAdmin(admin.ModelAdmin):
    list_display = ('character_from', 'character_to', 'relationship_type')
    list_filter = ('relationship_type',)
    search_fields = ('character_from__name', 'character_to__name', 'description')


@admin.register(StoryStructure)
class StoryStructureAdmin(admin.ModelAdmin):
    list_display = ('book', 'story_structure', 'chapter_count', 'chapter_length', 'outline_approved', 'generation_strategy')
    list_filter = ('story_structure', 'outline_approved', 'generation_strategy')
    search_fields = ('book__title',)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_number', 'title', 'book', 'status', 'estimated_words', 'actual_words', 'generation_order', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'summary', 'outline', 'book__title')
    inlines = [RevisionHistoryInline]
    ordering = ('book', 'chapter_number')


@admin.register(PlotPoint)
class PlotPointAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'chapter', 'importance', 'resolved')
    list_filter = ('importance', 'resolved')
    search_fields = ('title', 'description', 'book__title')


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'title', 'book', 'chapter', 'date')
    search_fields = ('title', 'description', 'date', 'book__title')
    ordering = ('book', 'sequence')


@admin.register(AIWritingStyle)
class AIWritingStyleAdmin(admin.ModelAdmin):
    list_display = ('book', 'pov', 'tense', 'tone', 'dialogue_level', 'description_level', 'pacing')
    list_filter = ('pov', 'tense', 'dialogue_level', 'description_level')
    search_fields = ('book__title', 'tone', 'writing_style', 'custom_instructions')


@admin.register(AIGenerationSettings)
class AIGenerationSettingsAdmin(admin.ModelAdmin):
    list_display = ('book', 'generation_mode', 'creativity', 'strictness', 'temperature', 'chapter_word_target', 'auto_approve')
    list_filter = ('generation_mode', 'generate_summaries_first', 'auto_approve')
    search_fields = ('book__title',)


@admin.register(CharacterMemory)
class CharacterMemoryAdmin(admin.ModelAdmin):
    list_display = ('key', 'character', 'importance', 'updated_at')
    search_fields = ('key', 'value', 'character__name')
    list_filter = ('importance',)


@admin.register(WorldMemory)
class WorldMemoryAdmin(admin.ModelAdmin):
    list_display = ('key', 'world', 'importance', 'updated_at')
    search_fields = ('key', 'value', 'world__book__title')
    list_filter = ('importance',)


@admin.register(TimelineMemory)
class TimelineMemoryAdmin(admin.ModelAdmin):
    list_display = ('key', 'book', 'importance', 'updated_at')
    search_fields = ('key', 'value', 'book__title')
    list_filter = ('importance',)


@admin.register(LoreMemory)
class LoreMemoryAdmin(admin.ModelAdmin):
    list_display = ('key', 'book', 'importance', 'updated_at')
    search_fields = ('key', 'value', 'book__title')
    list_filter = ('importance',)


@admin.register(UploadedAsset)
class UploadedAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'asset_type', 'file_size', 'uploaded_at')
    list_filter = ('asset_type', 'uploaded_at')
    search_fields = ('title', 'description', 'book__title')


@admin.register(ExportHistory)
class ExportHistoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'format', 'status', 'export_date')
    list_filter = ('format', 'status', 'export_date')
    search_fields = ('book__title',)


@admin.register(RevisionHistory)
class RevisionHistoryAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'reason', 'timestamp')
    search_fields = ('chapter__title', 'reason', 'old_text', 'new_text')
    readonly_fields = ('chapter', 'old_text', 'new_text', 'reason', 'timestamp')
