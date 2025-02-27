from dataclasses import dataclass
from typing import List, Dict, Optional, Any

class Metabase:

    def __init__(self, hook):
        self.hook = hook
        self.databases = hook.get_databases()
        self.tables = hook.get_tables()
        self.fields = self.get_databases_fields()

        self.cards = hook.get_cards()

        # self.cards = [
        #     card for card in self.cards if card['id'] == 38
        # ]

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
