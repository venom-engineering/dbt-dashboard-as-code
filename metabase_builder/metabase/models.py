import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


class Metabase:

    def __init__(self, hook):
        self.hook = hook

        self.refresh_state()

    def refresh_state(self):

        # TODO: Dict or List for objects?

        # Get all Metabase objects
        self.databases = self.hook.get_databases()
        self.tables = self.hook.get_tables()
        self.fields = self.get_databases_fields()

        self.cards = self.hook.get_cards()

        self.dashboards = ...
        self.users = ...  # ?
        self.tiles = ...  # ?
        self.datasets = ...  # ?

        # TODO: Maps objects
        ...

    def get_databases_fields(self):
        fields = {}
        for database_id, _ in self.databases.items():
            fields.update(self.hook.get_database_fields(database_id=database_id))
        return fields


@dataclass
class Field:
    '''
    Represents a field within a table in Metabase.
    '''

    id: int
    name: str
    display_name: str
    base_type: str
    semantic_type: Optional[str]
    table_name: str
    table_id: int
    schema: str

@dataclass
class Table:
    '''
    Represents a table in Metabase.
    '''
    # Primary Identifiers
    id: int
    name: str
    display_name: str

    # Database Information
    db_id: int
    db: Any  # TODO: how to override it in a clean way?

    # Basic Information
    description: Optional[str]
    schema: str
    entity_type: str

    # Sync and Update Details
    initial_sync_status: str  # Initial synchronization status (e.g., "complete")
    updated_at: str  # Timestamp of the last update
    created_at: str  # Timestamp of creation

    # Visibility and Access
    visibility_type: Optional[str]
    show_in_getting_started: bool
    active: bool

    # Other
    view_count: int
    caveats: Optional[Any]
    field_order: str
    is_upload: bool
    estimated_row_count: Optional[int]
    points_of_interest: Optional[str]
    database_require_filter: bool


@dataclass
class Database:
    '''
    Represents a database in Metabase.
    '''

    # Primary Identifiers
    id: int
    name: str

    # Basic Information
    description: Optional[str]
    engine: str
    dbms_version: Any

    # Sync and Update Details
    initial_sync_status: str
    is_full_sync: bool
    updated_at: str
    created_at: str
    metadata_sync_schedule: str
    cache_field_values_schedule: str

    # Features and Permissions
    features: List[str]
    native_permissions: str

    # Advanced Configurations
    details: Dict
    settings: Optional[Any]
    caveats: Optional[Any]

    # Uploads
    uploads_enabled: bool
    uploads_schema_name: Optional[str]
    uploads_table_prefix: Optional[str]
    can_upload: bool

    # Cache
    cache_ttl: Any

    # Status and Flags
    is_attached_dwh: bool
    auto_run_queries: bool
    is_sample: bool
    is_on_demand: bool
    is_audit: bool

    # Other
    timezone: str
    points_of_interest: str
    refingerprint: str
    creator_id: int

@dataclass
class Creator:
    """Represents the creator of a Metabase card."""
    email: str
    first_name: str
    last_login: Optional[str]
    is_qbnewb: bool
    is_superuser: bool
    id: int
    last_name: str
    date_joined: str
    common_name: str


@dataclass
class ResultMetadata:
    """Represents metadata about a result field in a Metabase card."""
    description: Optional[str]
    semantic_type: str
    coercion_strategy: Optional[Any]
    name: str
    settings: Optional[Any]
    fk_target_field_id: Optional[int]
    field_ref: List
    effective_type: str
    id: int
    visibility_type: str
    display_name: str
    base_type: str
    # Add other potential fields like `unit` and `converted_timezone` if needed


@dataclass
class Collection:
    """Represents a collection in Metabase."""
    authority_level: Optional[Any]
    description: str
    archived: bool
    slug: str
    archive_operation_id: Optional[Any]
    name: str
    personal_owner_id: Optional[Any]
    type: Optional[Any]
    is_sample: bool
    id: int
    archived_directly: Optional[Any]
    entity_id: str
    location: str
    namespace: Optional[Any]
    created_at: str


@dataclass
class DatasetQuery:
    """Represents the dataset query for a Metabase card."""
    database: int
    type: str
    query: Dict  # This could be further broken down into a separate dataclass if needed


@dataclass
class Card:
    """Represents a Metabase card."""
    id: int
    name: str
    display: str
    description: str
    archived: bool
    view_count: int
    table_id: Optional[int]
    creator: Creator
    database_id: int
    collection_id: int
    query_type: str
    type: str
    creator_id: int
    updated_at: str
    dataset_query: DatasetQuery
    visualization_settings: Dict
    collection: Collection

    # Optional fields with default values
    cache_invalidated_at: Optional[str] = None
    collection_position: Optional[int] = None
    source_card_id: Optional[int] = None
    result_metadata: Optional[List[ResultMetadata]] = None
    initially_published_at: Optional[str] = None
    enable_embedding: bool = False
    last_used_at: Optional[str] = None
    made_public_by_id: Optional[int] = None
    embedding_params: Optional[Any] = None
    cache_ttl: Optional[Any] = None
    parameter_mappings: Optional[List] = None
    archived_directly: bool = False
    entity_id: Optional[str] = None
    collection_preview: bool = False
    metabase_version: Optional[str] = None
    parameters: Optional[List] = None
    dashboard_id: Optional[int] = None
    created_at: Optional[str] = None
    public_uuid: Optional[str] = None

    exposure_unique_id: Optional[str] = field(init=False, default=None)

    def __post_init__(self):

        # Find match to exposure unique ID if exists
        pattern = r"exposure_unique_id:\s*(.*)"
        match = re.search(pattern, self.description or '', flags=re.MULTILINE)
        if match:
            self.exposure_unique_id = match.group(1)
