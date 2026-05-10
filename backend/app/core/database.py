"""
Supabase database connection and operations
"""
from supabase import create_client, Client
from app.core.config import settings
from typing import List, Dict, Any, Optional

class SupabaseDB:
    """Supabase database client wrapper"""
    
    _instance: Optional['SupabaseDB'] = None
    _client: Optional[Client] = None
    _init_error: Optional[Exception] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseDB, cls).__new__(cls)
        return cls._instance
    
    def _initialize(self):
        """Initialize Supabase client"""
        try:
            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY
            )
            self._init_error = None
        except Exception as exc:
            self._client = None
            self._init_error = exc
    
    @property
    def client(self) -> Client:
        """Get Supabase client"""
        if self._client is None:
            self._initialize()
        if self._client is None:
            raise RuntimeError(
                f"Supabase client is not configured correctly: {self._init_error}"
            )
        return self._client
    
    def select(self, table: str, columns: str = "*") -> Any:
        """Select data from table"""
        return self.client.table(table).select(columns)
    
    def insert(self, table: str, data: Dict[str, Any]) -> Any:
        """Insert data into table"""
        return self.client.table(table).insert(data).execute()
    
    def update(self, table: str, data: Dict[str, Any], id: str) -> Any:
        """Update data in table"""
        return self.client.table(table).update(data).eq("id", id).execute()
    
    def delete(self, table: str, id: str) -> Any:
        """Delete data from table"""
        return self.client.table(table).delete().eq("id", id).execute()
    
    def query(self, table: str) -> Any:
        """Get query builder for table"""
        return self.client.table(table)

# Singleton instance
db = SupabaseDB()

def get_db() -> SupabaseDB:
    """Dependency injection for database"""
    return db
