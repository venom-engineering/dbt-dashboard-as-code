import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# TODO: Sub definitions must be overriden everywhere in post-init.

@dataclass
class MetabaseDefinition:
    '''Represents a definition within a Metabase Instance'''
    metabase: Any = field(init=True, repr=False, compare=False)



@dataclass
class Database(MetabaseDefinition):
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

    # After init mappings
    tables: List['Table'] = field(init=False, default_factory=list)



@dataclass
class Table(MetabaseDefinition):
    '''
    Represents a table in Metabase.
    '''
    # Primary Identifiers
    id: int
    name: str
    display_name: str

    # Database Information
    db_id: int

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

    # After init mappings
    db: Database = field(init=True)  # As is it sent from API.
    fields: List['Field'] = field(init=False, default_factory=list)

    def __post_init__(self):
        db = self.metabase.get_database_by_id(self.db_id)
        self.db = db
        db.tables.append(self)

@dataclass
class Field(MetabaseDefinition):
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

    # After init mappings
    table: Table = field(init=False)

    def __post_init__(self):
        table = self.metabase.get_table_by_id(self.table_id)
        self.table = table
        table.fields.append(self)

@dataclass
class Creator(MetabaseDefinition):
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
class ResultMetadata(MetabaseDefinition):
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
class Collection(MetabaseDefinition):
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
class DatasetQuery(MetabaseDefinition):
    """Represents the dataset query for a Metabase card."""
    database: int
    type: str
    query: Dict  # This could be further broken down into a separate dataclass if needed


@dataclass
class Card(MetabaseDefinition):
    """Represents a Metabase card."""
    id: int
    name: str
    display: str
    description: str
    archived: bool
    view_count: int
    table_id: int
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

    # After init mappings
    table: Table = field(init=False)
    exposure_unique_id: Optional[str] = field(init=False, default=None)

    def __post_init__(self):
        table = self.metabase.get_table_by_id(self.table_id)
        self.table = table

        # Find match to exposure unique ID if exists
        pattern = r"exposure_unique_id:\s*(.*)"
        match = re.search(pattern, self.description or '', flags=re.MULTILINE)
        if match:
            self.exposure_unique_id = match.group(1)
