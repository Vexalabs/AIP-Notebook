"""
Database Service

Handles database connections and credentials management.
Integrates with the config system to fetch credentials from:
1. Local config file (.secrets/config.json)
2. Google Secret Manager
3. Environment variables
"""

import os
import json
import mysql.connector
from typing import Optional, Dict, Any
from pathlib import Path
import logging
from contextlib import contextmanager

# Try to import config, but allow standalone usage
try:
    from backend.config import config
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for managing database connections and credentials."""
    
    def __init__(
        self,
        host: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        port: int = 3306,
        use_config: bool = True
    ):
        """
        Initialize Database Service.
        
        Priority order for credentials:
        1. Explicitly passed parameters
        2. Config system (if use_config=True)
        3. Environment variables
        
        Args:
            host: Database host
            user: Database user
            password: Database password
            database: Database name
            port: Database port (default: 3306)
            use_config: Whether to use the config system (default: True)
        """
        self.port = port
        
        # Try to get from config system first if enabled
        if use_config and HAS_CONFIG:
            self._load_from_config()
        
        # Override with explicit parameters or environment variables
        self.host = host or self._get_from_env('DB_HOST') or getattr(self, 'host', None)
        self.user = user or self._get_from_env('DB_USER') or getattr(self, 'user', None)
        self.password = password or self._get_from_env('DB_PASSWORD') or getattr(self, 'password', None)
        self.database = database or self._get_from_env('DB_NAME') or getattr(self, 'database', 'PMP_Backend')
        
        # Validate we have required credentials
        if not all([self.host, self.user, self.password]):
            missing = []
            if not self.host: missing.append('host')
            if not self.user: missing.append('user')
            if not self.password: missing.append('password')
            
            logger.warning(f"Missing database credentials: {', '.join(missing)}")
            logger.info("Provide credentials via: constructor args, config file, or environment variables")
    
    def _get_from_env(self, key: str) -> Optional[str]:
        """Get value from environment variable."""
        return os.getenv(key)
    
    def _load_from_config(self):
        """Load database credentials from config system."""
        try:
            app_config = config.get()
            
            if app_config.database and app_config.database.connection_string:
                # Parse connection string if available
                # Format: mysql://user:password@host:port/database
                conn_str = app_config.database.connection_string
                self._parse_connection_string(conn_str)
                logger.info("Loaded database config from connection string")
            else:
                # Try to get from secrets or other config sources
                logger.debug("No database connection string in config")
                
        except Exception as e:
            logger.debug(f"Could not load from config system: {e}")
    
    def _parse_connection_string(self, conn_str: str):
        """Parse MySQL connection string."""
        try:
            # Remove mysql:// prefix
            if conn_str.startswith('mysql://'):
                conn_str = conn_str[8:]
            
            # Split user:password@host:port/database
            if '@' in conn_str:
                auth, location = conn_str.split('@', 1)
                if ':' in auth:
                    self.user, self.password = auth.split(':', 1)
                
                if '/' in location:
                    host_port, self.database = location.split('/', 1)
                    if ':' in host_port:
                        self.host, port_str = host_port.split(':', 1)
                        self.port = int(port_str)
                    else:
                        self.host = host_port
                else:
                    if ':' in location:
                        self.host, port_str = location.split(':', 1)
                        self.port = int(port_str)
                    else:
                        self.host = location
                        
        except Exception as e:
            logger.error(f"Failed to parse connection string: {e}")
    
    def get_connection_params(self) -> Dict[str, Any]:
        """
        Get connection parameters as a dictionary.
        
        Returns:
            Dictionary with connection parameters
        """
        return {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'port': self.port
        }
    
    def create_connection(self) -> mysql.connector.MySQLConnection:
        """
        Create and return a new database connection.
        
        Returns:
            MySQL connection object
            
        Raises:
            mysql.connector.Error: If connection fails
        """
        try:
            conn = mysql.connector.connect(**self.get_connection_params())
            logger.debug(f"Connected to database: {self.database}@{self.host}")
            return conn
        except mysql.connector.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Automatically closes connection when done.
        
        Usage:
            with db_service.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        conn = None
        try:
            conn = self.create_connection()
            yield conn
        finally:
            if conn and conn.is_connected():
                conn.close()
                logger.debug("Database connection closed")
    
    @contextmanager
    def get_cursor(self, dictionary=True):
        """
        Context manager for database cursor.
        Automatically handles connection and cursor cleanup.
        
        Args:
            dictionary: If True, return rows as dictionaries (default: True)
            
        Usage:
            with db_service.get_cursor() as cursor:
                cursor.execute("SELECT * FROM table")
                results = cursor.fetchall()
        """
        conn = None
        cursor = None
        try:
            conn = self.create_connection()
            cursor = conn.cursor(dictionary=dictionary)
            yield cursor
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                logger.info("✓ Database connection test successful")
                return True
        except Exception as e:
            logger.error(f"✗ Database connection test failed: {e}")
            return False
    
    def __repr__(self):
        """String representation (hides password)."""
        return f"DatabaseService(host={self.host}, user={self.user}, database={self.database})"


# Global instance for convenience
_db_service = None

def get_database_service(
    host: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
    use_config: bool = True
) -> DatabaseService:
    """
    Get or create a global DatabaseService instance.
    
    Args:
        host: Database host (optional)
        user: Database user (optional)
        password: Database password (optional)
        database: Database name (optional)
        use_config: Whether to use config system (default: True)
        
    Returns:
        DatabaseService instance
    """
    global _db_service
    
    # If parameters provided, create new instance
    if any([host, user, password, database]):
        return DatabaseService(
            host=host,
            user=user,
            password=password,
            database=database,
            use_config=use_config
        )
    
    # Otherwise use/create global instance
    if _db_service is None:
        _db_service = DatabaseService(use_config=use_config)
    
    return _db_service
