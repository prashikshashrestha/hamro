import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# ==============================================================================
# ENUMS / TEXT CHOICES
# ==============================================================================

class BookStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    OUTLINE = 'outline', 'Outline'
    WRITING = 'writing', 'Writing'
    COMPLETED = 'completed', 'Completed'
    ARCHIVED = 'archived', 'Archived'


class BookType(models.TextChoices):
    FICTION = 'fiction', 'Fiction'
    NON_FICTION = 'non_fiction', 'Non-Fiction'
    MEMOIR = 'memoir', 'Memoir'
    CHILDRENS = 'childrens', "Children's"
    EDUCATIONAL = 'educational', 'Educational'
    POETRY = 'poetry', 'Poetry'
    SHORT_STORY = 'short_story', 'Short Story'
    ESSAY = 'essay', 'Essay / Article Collection'
    GRAPHIC_NOVEL = 'graphic_novel', 'Graphic Novel / Comic Script'
    OTHER = 'other', 'Other'


class ImportanceLevel(models.TextChoices):
    CRITICAL = 'critical', 'Critical'
    MAJOR = 'major', 'Major'
    MEDIUM = 'medium', 'Medium'
    MINOR = 'minor', 'Minor'
    BACKGROUND = 'background', 'Background'


class CharacterRole(models.TextChoices):
    PROTAGONIST = 'protagonist', 'Protagonist'
    ANTAGONIST = 'antagonist', 'Antagonist'
    DEUTERAGONIST = 'deuteragonist', 'Deuteragonist'
    SUPPORTING = 'supporting', 'Supporting'
    MENTOR = 'mentor', 'Mentor'
    FOIL = 'foil', 'Foil'
    LOVE_INTEREST = 'love_interest', 'Love Interest'
    MINOR = 'minor', 'Minor / Cameo'


class RelationshipType(models.TextChoices):
    ALLY = 'ally', 'Ally'
    ENEMY = 'enemy', 'Enemy'
    RIVAL = 'rival', 'Rival'
    FAMILY = 'family', 'Family'
    LOVER = 'lover', 'Lover / Romantic'
    MENTOR_STUDENT = 'mentor_student', 'Mentor / Student'
    FRIEND = 'friend', 'Friend'
    ACQUAINTANCE = 'acquaintance', 'Acquaintance'
    OTHER = 'other', 'Other'


class StructureType(models.TextChoices):
    THREE_ACT = 'three_act', 'Three-Act Structure'
    HEROS_JOURNEY = 'heros_journey', "Hero's Journey"
    SAVE_THE_CAT = 'save_the_cat', 'Save the Cat!'
    DAN_HARMON_CIRCLE = 'dan_harmon_circle', 'Dan Harmon Story Circle'
    SNOWFLAKE = 'snowflake', 'Snowflake Method'
    FIVE_ACT = 'five_act', 'Five-Act Structure (Freytag Pyramid)'
    KISHOTENKETSU = 'kishotenketsu', 'Kishōtenketsu (4-Act)'
    NON_FICTION_TOPIC = 'non_fiction_topic', 'Non-Fiction Topic-Based'
    CHRONOLOGICAL = 'chronological', 'Chronological / Memoir'
    CUSTOM = 'custom', 'Custom Structure'


class GenerationStrategy(models.TextChoices):
    SEQUENTIAL = 'sequential', 'Sequential (Chapter by Chapter)'
    OUTLINE_FIRST = 'outline_first', 'Outline First, Then Content'
    HIERARCHICAL = 'hierarchical', 'Hierarchical (High-level to Detail)'
    SCENE_BY_SCENE = 'scene_by_scene', 'Scene by Scene'


class ChapterStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    OUTLINED = 'outlined', 'Outlined'
    DRAFTING = 'drafting', 'Drafting in Progress'
    POLISHING = 'polishing', 'Polishing / Pass 2'
    COMPLETED = 'completed', 'Completed'
    REVISION_REQUESTED = 'revision_requested', 'Revision Requested'


class PlotPointImportance(models.TextChoices):
    INCITING_INCIDENT = 'inciting_incident', 'Inciting Incident'
    FIRST_PLOT_POINT = 'first_plot_point', 'First Plot Point'
    MIDPOINT = 'midpoint', 'Midpoint'
    SECOND_PLOT_POINT = 'second_plot_point', 'Second Plot Point'
    CLIMAX = 'climax', 'Climax'
    RESOLUTION = 'resolution', 'Resolution'
    MINOR = 'minor', 'Minor Plot Beat'


class POVType(models.TextChoices):
    FIRST_PERSON = 'first_person', 'First Person (I/We)'
    THIRD_PERSON_LIMITED = 'third_person_limited', 'Third Person Limited (He/She/They)'
    THIRD_PERSON_OMNISCIENT = 'third_person_omniscient', 'Third Person Omniscient'
    SECOND_PERSON = 'second_person', 'Second Person (You)'


class TenseType(models.TextChoices):
    PAST = 'past', 'Past Tense'
    PRESENT = 'present', 'Present Tense'
    FUTURE = 'future', 'Future Tense'


class DetailLevel(models.TextChoices):
    MINIMAL = 'minimal', 'Minimal'
    MODERATE = 'moderate', 'Moderate'
    HIGH = 'high', 'High / Detailed'
    INTENSE = 'intense', 'Intense / Rich'


class GenMode(models.TextChoices):
    AUTOMATIC = 'automatic', 'Fully Automatic'
    SEMI_AUTO = 'semi_auto', 'Semi-Automatic (Interactive Approval)'
    STEP_BY_STEP = 'step_by_step', 'Step-by-Step'
    MANUAL = 'manual', 'Manual Trigger'


class AssetType(models.TextChoices):
    PDF = 'pdf', 'PDF Document'
    DOCX = 'docx', 'Word Document (DOCX)'
    TXT = 'txt', 'Plain Text File'
    MARKDOWN = 'markdown', 'Markdown File'
    IMAGE = 'image', 'Reference Image'
    MAP = 'map', 'World / Regional Map'
    REFERENCE = 'reference', 'Research Reference Material'


class ExportFormat(models.TextChoices):
    PDF = 'pdf', 'PDF'
    EPUB = 'epub', 'EPUB'
    MOBI = 'mobi', 'MOBI'
    DOCX = 'docx', 'Microsoft Word (DOCX)'
    MARKDOWN = 'markdown', 'Markdown'
    HTML = 'html', 'HTML'
    TXT = 'txt', 'Plain Text'


class ExportStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'


# ==============================================================================
# 1. BOOK SERIES
# ==============================================================================

class Series(models.Model):
    """
    Groups multiple related books under a unified series umbrella.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='series',
        verbose_name="Owner"
    )
    name = models.CharField(max_length=255, verbose_name="Series Name")
    description = models.TextField(blank=True, verbose_name="Series Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['name']
        verbose_name = "Book Series"
        verbose_name_plural = "Book Series"
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_series_name')
        ]

    def __str__(self):
        return self.name


# ==============================================================================
# 2. TAGS
# ==============================================================================

class Tag(models.Model):
    """
    Categorization tags for books (e.g., Magic, War, Politics, Dragons).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name="Tag Name")
    slug = models.SlugField(max_length=60, unique=True, verbose_name="Tag Slug")

    class Meta:
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        indexes = [
            models.Index(fields=['slug'], name='tag_slug_idx'),
        ]

    def __str__(self):
        return self.name


# ==============================================================================
# 3. BOOK
# ==============================================================================

class Book(models.Model):
    """
    Core Book model representing a single literary work (Novel, Short Story, Non-Fiction, Memoir, etc.).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Owner"
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name="Series"
    )
    series_order = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Order in Series",
        help_text="Volume / Book number within the series"
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Subtitle")
    slug = models.SlugField(max_length=255, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description / Blurb")
    language = models.CharField(max_length=10, default='en', verbose_name="Language")
    
    status = models.CharField(
        max_length=20,
        choices=BookStatus.choices,
        default=BookStatus.DRAFT,
        db_index=True,
        verbose_name="Status"
    )
    book_type = models.CharField(
        max_length=30,
        choices=BookType.choices,
        default=BookType.FICTION,
        db_index=True,
        verbose_name="Book Type"
    )
    genre = models.CharField(max_length=100, verbose_name="Primary Genre")
    subgenre = models.CharField(max_length=100, blank=True, verbose_name="Subgenre")
    target_audience = models.CharField(max_length=100, blank=True, verbose_name="Target Audience")
    reading_level = models.CharField(max_length=50, blank=True, verbose_name="Reading Level")
    
    estimated_word_count = models.PositiveIntegerField(default=0, verbose_name="Estimated Word Count")
    actual_word_count = models.PositiveIntegerField(default=0, verbose_name="Actual Word Count")
    
    tags = models.ManyToManyField(Tag, blank=True, related_name='books', verbose_name="Tags")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        constraints = [
            models.UniqueConstraint(fields=['user', 'slug'], name='unique_user_book_slug')
        ]
        indexes = [
            models.Index(fields=['user', 'status'], name='book_user_status_idx'),
            models.Index(fields=['user', 'book_type'], name='book_user_type_idx'),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_book_type_display()})"


# ==============================================================================
# 4. BOOK PROFILE (CREATIVE DIRECTION)
# ==============================================================================

class BookProfile(models.Model):
    """
    Stores high-level creative direction, themes, premise, and constraints for a book.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Book"
    )
    premise = models.TextField(blank=True, verbose_name="Premise")
    logline = models.TextField(blank=True, verbose_name="Logline")
    summary = models.TextField(blank=True, verbose_name="Executive Summary")
    themes = models.TextField(
        blank=True,
        verbose_name="Core Themes",
        help_text="Central themes, moral questions, or subtexts"
    )
    central_conflict = models.TextField(blank=True, verbose_name="Central Conflict")
    ending_preference = models.TextField(
        blank=True,
        verbose_name="Ending Preference",
        help_text="e.g. Bittersweet, Happy Ending, Cliffhanger, Open Resolution"
    )
    inspirations = models.TextField(
        blank=True,
        verbose_name="Inspirations",
        help_text="Comparative titles, authors, or stylistic influences"
    )
    must_include = models.TextField(
        blank=True,
        verbose_name="Must Include",
        help_text="Key tropes, elements, or scenes that must be present"
    )
    must_avoid = models.TextField(
        blank=True,
        verbose_name="Must Avoid",
        help_text="Tropes, cliches, or trigger elements to strictly exclude"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Book Profile"
        verbose_name_plural = "Book Profiles"

    def __str__(self):
        return f"Profile for {self.book.title}"


# ==============================================================================
# 5. WORLD BUILDING & LOCATIONS
# ==============================================================================

class WorldBuilding(models.Model):
    """
    World-building configuration (specifically for fiction/fantasy/sci-fi world context).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='world_building',
        verbose_name="Book"
    )
    world_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="World Type",
        help_text="e.g. High Fantasy, Cyberpunk, Dystopian Earth, Alternate History"
    )
    setting = models.TextField(blank=True, verbose_name="Overall Setting")
    era = models.CharField(max_length=100, blank=True, verbose_name="Era")
    time_period = models.CharField(max_length=100, blank=True, verbose_name="Time Period")
    technology_level = models.CharField(max_length=100, blank=True, verbose_name="Technology Level")
    magic_system = models.TextField(blank=True, verbose_name="Magic / Supernatural System")
    politics = models.TextField(blank=True, verbose_name="Politics & Factions")
    religion = models.TextField(blank=True, verbose_name="Religion & Belief Systems")
    economy = models.TextField(blank=True, verbose_name="Economy & Commerce")
    cultures = models.TextField(blank=True, verbose_name="Cultures & Traditions")
    languages = models.TextField(blank=True, verbose_name="Languages & Linguistics")
    world_rules = models.TextField(
        blank=True,
        verbose_name="World Rules & Laws",
        help_text="Core physical, magical, or societal rules governing the world"
    )
    atmosphere = models.TextField(
        blank=True,
        verbose_name="Atmosphere & Sensory Details",
        help_text="Mood, visual aesthetics, soundscapes, and sensory elements"
    )
    notes = models.TextField(blank=True, verbose_name="Additional Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "World Building"
        verbose_name_plural = "World Building"

    def __str__(self):
        return f"World Building for {self.book.title}"


class Location(models.Model):
    """
    Individual key locations belonging to a specific WorldBuilding entity.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    world = models.ForeignKey(
        WorldBuilding,
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name="World"
    )
    name = models.CharField(max_length=255, verbose_name="Location Name")
    description = models.TextField(blank=True, verbose_name="Description")
    importance = models.CharField(
        max_length=20,
        choices=ImportanceLevel.choices,
        default=ImportanceLevel.MEDIUM,
        verbose_name="Importance Level"
    )
    coordinates = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Coordinates / Spatial Data",
        help_text="Optional JSON coordinates e.g. {'x': 120, 'y': 450} or lat/long"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['name']
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        indexes = [
            models.Index(fields=['world', 'name'], name='loc_world_name_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_importance_display()})"


# ==============================================================================
# 6. CHARACTERS & CHARACTER RELATIONSHIPS
# ==============================================================================

class Character(models.Model):
    """
    Individual character profile belonging to a book.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='characters',
        verbose_name="Book"
    )
    name = models.CharField(max_length=255, verbose_name="Character Name")
    role = models.CharField(
        max_length=30,
        choices=CharacterRole.choices,
        default=CharacterRole.SUPPORTING,
        db_index=True,
        verbose_name="Role"
    )
    age = models.CharField(max_length=50, blank=True, verbose_name="Age")
    gender = models.CharField(max_length=50, blank=True, verbose_name="Gender")
    personality = models.TextField(blank=True, verbose_name="Personality Traits")
    appearance = models.TextField(blank=True, verbose_name="Physical Appearance")
    background = models.TextField(blank=True, verbose_name="Backstory / History")
    goal = models.TextField(blank=True, verbose_name="Primary Goal / Motivation")
    fear = models.TextField(blank=True, verbose_name="Greatest Fear")
    strengths = models.TextField(blank=True, verbose_name="Key Strengths")
    weaknesses = models.TextField(blank=True, verbose_name="Key Weaknesses")
    internal_conflict = models.TextField(blank=True, verbose_name="Internal Conflict")
    external_conflict = models.TextField(blank=True, verbose_name="External Conflict")
    speech_style = models.TextField(blank=True, verbose_name="Speech Style / Voice")
    habits = models.TextField(blank=True, verbose_name="Quirks & Habits")
    secrets = models.TextField(blank=True, verbose_name="Secrets")
    character_arc = models.TextField(blank=True, verbose_name="Character Arc Transformation")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['role', 'name']
        verbose_name = "Character"
        verbose_name_plural = "Characters"
        indexes = [
            models.Index(fields=['book', 'role'], name='char_book_role_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class CharacterRelationship(models.Model):
    """
    Normalized relationship link between two characters in a book.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    character_from = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='relationships_from',
        verbose_name="Source Character"
    )
    character_to = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='relationships_to',
        verbose_name="Target Character"
    )
    relationship_type = models.CharField(
        max_length=30,
        choices=RelationshipType.choices,
        default=RelationshipType.ALLY,
        verbose_name="Relationship Type"
    )
    description = models.TextField(blank=True, verbose_name="Relationship Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Character Relationship"
        verbose_name_plural = "Character Relationships"
        constraints = [
            models.UniqueConstraint(
                fields=['character_from', 'character_to'],
                name='unique_character_relationship'
            ),
            models.CheckConstraint(
                check=~models.Q(character_from=models.F('character_to')),
                name='prevent_self_relationship'
            )
        ]

    def __str__(self):
        return f"{self.character_from.name} -> {self.character_to.name} ({self.get_relationship_type_display()})"


# ==============================================================================
# 7. STORY STRUCTURE, CHAPTERS, PLOT POINTS & TIMELINE
# ==============================================================================

class StoryStructure(models.Model):
    """
    Defines the structural blueprint and generation strategy for a book.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='story_structure',
        verbose_name="Book"
    )
    story_structure = models.CharField(
        max_length=50,
        choices=StructureType.choices,
        default=StructureType.THREE_ACT,
        verbose_name="Story Structure Paradigm"
    )
    chapter_count = models.PositiveIntegerField(default=12, verbose_name="Target Chapter Count")
    chapter_length = models.PositiveIntegerField(
        default=2500,
        verbose_name="Target Chapter Length (Words)"
    )
    outline_approved = models.BooleanField(default=False, verbose_name="Outline Approved")
    generation_mode = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Custom Generation Mode"
    )
    generation_strategy = models.CharField(
        max_length=50,
        choices=GenerationStrategy.choices,
        default=GenerationStrategy.OUTLINE_FIRST,
        verbose_name="Generation Strategy"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Story Structure"
        verbose_name_plural = "Story Structures"

    def __str__(self):
        return f"Structure for {self.book.title} ({self.get_story_structure_display()})"


class Chapter(models.Model):
    """
    Represents an individual chapter within a book.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name="Book"
    )
    chapter_number = models.PositiveIntegerField(verbose_name="Chapter Number")
    generation_order = models.PositiveIntegerField(
        default=1,
        verbose_name="Generation Order",
        help_text="Order in which this chapter is queue-processed during AI generation"
    )
    title = models.CharField(max_length=255, verbose_name="Chapter Title")
    summary = models.TextField(blank=True, verbose_name="Chapter Summary")
    outline = models.TextField(blank=True, verbose_name="Detailed Chapter Outline / Scenes")
    generated_content = models.TextField(blank=True, verbose_name="Generated Chapter Content")
    
    status = models.CharField(
        max_length=30,
        choices=ChapterStatus.choices,
        default=ChapterStatus.PENDING,
        db_index=True,
        verbose_name="Status"
    )
    estimated_words = models.PositiveIntegerField(default=0, verbose_name="Estimated Words")
    actual_words = models.PositiveIntegerField(default=0, verbose_name="Actual Words")
    notes = models.TextField(blank=True, verbose_name="Author / AI Notes")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['chapter_number']
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        constraints = [
            models.UniqueConstraint(fields=['book', 'chapter_number'], name='unique_book_chapter_number')
        ]
        indexes = [
            models.Index(fields=['book', 'chapter_number'], name='chap_book_num_idx'),
            models.Index(fields=['book', 'status'], name='chap_book_status_idx'),
        ]

    def __str__(self):
        return f"Chapter {self.chapter_number}: {self.title}"


class PlotPoint(models.Model):
    """
    Tracks specific plot events, milestones, and turning points in a book.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='plot_points',
        verbose_name="Book"
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='plot_points',
        verbose_name="Associated Chapter"
    )
    title = models.CharField(max_length=255, verbose_name="Plot Point Title")
    description = models.TextField(blank=True, verbose_name="Plot Point Description")
    importance = models.CharField(
        max_length=30,
        choices=PlotPointImportance.choices,
        default=PlotPointImportance.MINOR,
        verbose_name="Importance"
    )
    resolved = models.BooleanField(default=False, verbose_name="Is Resolved?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Plot Point"
        verbose_name_plural = "Plot Points"
        indexes = [
            models.Index(fields=['book', 'resolved'], name='pp_book_resolved_idx'),
        ]

    def __str__(self):
        return f"{self.title} ({'Resolved' if self.resolved else 'Pending'})"


class TimelineEvent(models.Model):
    """
    Chronological timeline entry associated with a book's narrative sequence.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='timeline_events',
        verbose_name="Book"
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='timeline_events',
        verbose_name="Associated Chapter"
    )
    title = models.CharField(max_length=255, verbose_name="Event Title")
    description = models.TextField(blank=True, verbose_name="Event Description")
    date = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="In-Universe / Historical Date",
        help_text="e.g. 'Year 304, Third Age' or '1942-06-15'"
    )
    sequence = models.PositiveIntegerField(
        default=1,
        verbose_name="Chronological Sequence Number",
        help_text="Explicit integer ordering for chronological sorting"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['sequence']
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"
        indexes = [
            models.Index(fields=['book', 'sequence'], name='timeline_book_seq_idx'),
        ]

    def __str__(self):
        return f"Seq {self.sequence}: {self.title}"


# ==============================================================================
# 8. AI WRITING STYLE & GENERATION SETTINGS
# ==============================================================================

class AIWritingStyle(models.Model):
    """
    Configures tone, perspective, detail level, and prose rules for AI generation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='writing_style',
        verbose_name="Book"
    )
    pov = models.CharField(
        max_length=30,
        choices=POVType.choices,
        default=POVType.THIRD_PERSON_LIMITED,
        verbose_name="Point of View"
    )
    tense = models.CharField(
        max_length=20,
        choices=TenseType.choices,
        default=TenseType.PAST,
        verbose_name="Narrative Tense"
    )
    tone = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Overall Tone",
        help_text="e.g. Dark & Gritty, Lighthearted, Academic, Whimsical"
    )
    writing_style = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Prose Style",
        help_text="e.g. Minimalist (Hemingway), Descriptive, Poetic, Action-Oriented"
    )
    dialogue_level = models.CharField(
        max_length=20,
        choices=DetailLevel.choices,
        default=DetailLevel.MODERATE,
        verbose_name="Dialogue Frequency"
    )
    description_level = models.CharField(
        max_length=20,
        choices=DetailLevel.choices,
        default=DetailLevel.MODERATE,
        verbose_name="Sensory Description Level"
    )
    pacing = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Pacing Preference",
        help_text="e.g. Fast-Paced, Slow-Burn, Steady"
    )
    reading_level = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Target Reading Level",
        help_text="e.g. Young Adult, Adult, Grade 8, Professional"
    )
    vocabulary = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Vocabulary Style",
        help_text="e.g. Accessible, Literary, Technical, Period-Accurate"
    )
    violence_level = models.CharField(
        max_length=20,
        choices=DetailLevel.choices,
        default=DetailLevel.MINIMAL,
        verbose_name="Violence Level"
    )
    romance_level = models.CharField(
        max_length=20,
        choices=DetailLevel.choices,
        default=DetailLevel.MINIMAL,
        verbose_name="Romance / Sensuality Level"
    )
    custom_instructions = models.TextField(
        blank=True,
        verbose_name="Custom Prompt Instructions",
        help_text="Specific negative or positive prompt directives injected into AI context"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "AI Writing Style"
        verbose_name_plural = "AI Writing Styles"

    def __str__(self):
        return f"Writing Style for {self.book.title}"


class AIGenerationSettings(models.Model):
    """
    Hyperparameters and execution policies controlling the AI generation pipeline.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='generation_settings',
        verbose_name="Book"
    )
    generation_mode = models.CharField(
        max_length=30,
        choices=GenMode.choices,
        default=GenMode.SEMI_AUTO,
        verbose_name="Generation Mode"
    )
    creativity = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.70,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        verbose_name="Creativity Rating",
        help_text="0.00 (deterministic) to 1.00 (highly creative)"
    )
    strictness = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.80,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        verbose_name="Outline Strictness",
        help_text="Adherence strictness to outline and world rules (0.00 to 1.00)"
    )
    temperature = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.70,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)],
        verbose_name="Model Temperature"
    )
    chapter_word_target = models.PositiveIntegerField(
        default=2500,
        verbose_name="Chapter Word Target"
    )
    generate_summaries_first = models.BooleanField(
        default=True,
        verbose_name="Generate Summaries First",
        help_text="If True, AI builds section summaries prior to full prose drafting"
    )
    auto_approve = models.BooleanField(
        default=False,
        verbose_name="Auto-Approve Outlines & Drafts",
        help_text="If True, skips manual user confirmation step between passes"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "AI Generation Setting"
        verbose_name_plural = "AI Generation Settings"

    def __str__(self):
        return f"Gen Settings for {self.book.title}"


# ==============================================================================
# 9. AI MEMORY SYSTEM (KEY-VALUE FACT STORAGE FOR AI RETRIEVAL)
# ==============================================================================

class BaseMemoryModel(models.Model):
    """
    Abstract base model for key/value memory facts retrieved by AI during generation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, db_index=True, verbose_name="Fact / Key Name")
    value = models.TextField(verbose_name="Fact Content / Value")
    importance = models.PositiveIntegerField(
        default=1,
        verbose_name="Relevance Weight",
        help_text="Priority score (1-10) for AI prompt injection selection"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        abstract = True
        ordering = ['-importance', 'key']


class CharacterMemory(BaseMemoryModel):
    """
    Key/Value facts specifically anchored to a Character.
    """
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='memories',
        verbose_name="Character"
    )

    class Meta(BaseMemoryModel.Meta):
        verbose_name = "Character Memory"
        verbose_name_plural = "Character Memories"
        constraints = [
            models.UniqueConstraint(fields=['character', 'key'], name='unique_character_memory_key')
        ]

    def __str__(self):
        return f"[{self.character.name}] {self.key}"


class WorldMemory(BaseMemoryModel):
    """
    Key/Value facts specifically anchored to World Building.
    """
    world = models.ForeignKey(
        WorldBuilding,
        on_delete=models.CASCADE,
        related_name='memories',
        verbose_name="World Building"
    )

    class Meta(BaseMemoryModel.Meta):
        verbose_name = "World Memory"
        verbose_name_plural = "World Memories"
        constraints = [
            models.UniqueConstraint(fields=['world', 'key'], name='unique_world_memory_key')
        ]

    def __str__(self):
        return f"[{self.world.book.title} World] {self.key}"


class TimelineMemory(BaseMemoryModel):
    """
    Key/Value facts tracking narrative history and continuity events across a book.
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='timeline_memories',
        verbose_name="Book"
    )

    class Meta(BaseMemoryModel.Meta):
        verbose_name = "Timeline Memory"
        verbose_name_plural = "Timeline Memories"
        constraints = [
            models.UniqueConstraint(fields=['book', 'key'], name='unique_timeline_memory_key')
        ]

    def __str__(self):
        return f"[{self.book.title} Timeline] {self.key}"


class LoreMemory(BaseMemoryModel):
    """
    Key/Value facts storing general lore, mythology, and background knowledge for a book.
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='lore_memories',
        verbose_name="Book"
    )

    class Meta(BaseMemoryModel.Meta):
        verbose_name = "Lore Memory"
        verbose_name_plural = "Lore Memories"
        constraints = [
            models.UniqueConstraint(fields=['book', 'key'], name='unique_lore_memory_key')
        ]

    def __str__(self):
        return f"[{self.book.title} Lore] {self.key}"


# ==============================================================================
# 10. UPLOADED ASSETS, EXPORT HISTORY & REVISION HISTORY
# ==============================================================================

class UploadedAsset(models.Model):
    """
    Uploaded reference materials, PDFs, DOCX, maps, or markdown documents for a book.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='assets',
        verbose_name="Book"
    )
    title = models.CharField(max_length=255, verbose_name="Asset Title")
    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        default=AssetType.REFERENCE,
        db_index=True,
        verbose_name="Asset Type"
    )
    file = models.FileField(upload_to='book_assets/%Y/%m/', verbose_name="File Attachment")
    description = models.TextField(blank=True, verbose_name="Description")
    file_size = models.PositiveBigIntegerField(
        default=0,
        verbose_name="File Size (Bytes)",
        help_text="Recorded file size in bytes"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded At")

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Uploaded Asset"
        verbose_name_plural = "Uploaded Assets"
        indexes = [
            models.Index(fields=['book', 'asset_type'], name='asset_book_type_idx'),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_asset_type_display()})"


class ExportHistory(models.Model):
    """
    Logs history of book exports generated in various formats (PDF, EPUB, MOBI, DOCX, etc.).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='exports',
        verbose_name="Book"
    )
    format = models.CharField(
        max_length=20,
        choices=ExportFormat.choices,
        verbose_name="Export Format"
    )
    status = models.CharField(
        max_length=20,
        choices=ExportStatus.choices,
        default=ExportStatus.PENDING,
        verbose_name="Export Status"
    )
    file = models.FileField(
        upload_to='exports/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Exported File"
    )
    error_message = models.TextField(blank=True, verbose_name="Error Log / Message")
    export_date = models.DateTimeField(auto_now_add=True, verbose_name="Export Date")

    class Meta:
        ordering = ['-export_date']
        verbose_name = "Export History"
        verbose_name_plural = "Export Histories"
        indexes = [
            models.Index(fields=['book', '-export_date'], name='exp_book_date_idx'),
        ]

    def __str__(self):
        return f"Export {self.book.title} ({self.get_format_display()}) - {self.get_status_display()}"


class RevisionHistory(models.Model):
    """
    Audit log storing previous text versions and reasons for chapter revisions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='revisions',
        verbose_name="Chapter"
    )
    old_text = models.TextField(verbose_name="Previous Text Content")
    new_text = models.TextField(verbose_name="New Text Content")
    reason = models.TextField(
        blank=True,
        verbose_name="Revision Reason / Prompt",
        help_text="Explanation, author note, or AI feedback triggering this change"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Revision History"
        verbose_name_plural = "Revision Histories"
        indexes = [
            models.Index(fields=['chapter', '-timestamp'], name='rev_chap_time_idx'),
        ]

    def __str__(self):
        return f"Revision for {self.chapter} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
