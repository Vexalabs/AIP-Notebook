# Database Service Integration - Update

## ✅ What Changed

The image generation service has been updated to use a centralized **DatabaseService** for credential management. This provides better integration with the existing config system and more flexible credential handling.

## 🔧 New Database Service

### File: `backend/services/database.py`

A new database service that:
- ✅ Integrates with the existing config system (`backend/config.py`)
- ✅ Supports multiple credential sources (priority order):
  1. Explicitly passed parameters
  2. Config system (`.secrets/config.json` or Google Secret Manager)
  3. Environment variables
- ✅ Provides context managers for clean connection handling
- ✅ Automatic transaction management (commit/rollback)
- ✅ Connection pooling and cleanup

### Key Features

**Context Managers:**
```python
# Automatic connection management
with db_service.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table")

# Automatic cursor and transaction management
with db_service.get_cursor(dictionary=True) as cursor:
    cursor.execute("SELECT * FROM table")
    results = cursor.fetchall()
    # Auto-commits on success, auto-rollbacks on error
```

**Flexible Initialization:**
```python
# From environment variables
db = DatabaseService()

# From explicit parameters
db = DatabaseService(
    host='localhost',
    user='root',
    password='password'
)

# From config system
db = DatabaseService(use_config=True)

# Mix of both (parameters override config)
db = DatabaseService(
    host='localhost',  # Override
    use_config=True    # Use config for user/password
)
```

## 📝 Updated Files

### 1. `backend/services/image_generation_service.py`

**Changes:**
- ✅ Now uses `DatabaseService` instead of direct MySQL connections
- ✅ Database credentials are now **optional** (can use config/env)
- ✅ Cleaner code with context managers
- ✅ Automatic transaction management
- ✅ Better error handling

**Before:**
```python
def __init__(self, db_host: str, db_user: str, db_password: str, ...):
    self.db_config = {
        'host': db_host,
        'user': db_user,
        'password': db_password,
        'database': db_name
    }

def _get_db_connection(self):
    conn = mysql.connector.connect(**self.db_config)
    return conn

def fetch_articles_without_images(self):
    conn = None
    try:
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
```

**After:**
```python
def __init__(self, db_host: Optional[str] = None, 
             db_user: Optional[str] = None, 
             db_password: Optional[str] = None, 
             use_config: bool = True, ...):
    self.db_service = DatabaseService(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        use_config=use_config
    )

def fetch_articles_without_images(self):
    with self.db_service.get_cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
```

### 2. New Test Script

**File:** `backend/scripts/test_database_service.py`

Tests the database service and integration:
```bash
python backend/scripts/test_database_service.py
```

## 🚀 How to Use

### Option 1: Environment Variables (Recommended)

```bash
export DB_HOST=your-db-host
export DB_USER=your-db-user
export DB_PASSWORD=your-password
export DB_NAME=PMP_Backend

# Now you can initialize without parameters
python backend/scripts/generate_images.py
```

### Option 2: Config File

Create `.secrets/config.json`:
```json
{
  "database": {
    "connection_string": "mysql://user:password@host:3306/PMP_Backend"
  }
}
```

Then:
```python
service = ImageGenerationService(use_config=True)
```

### Option 3: Explicit Parameters (Backward Compatible)

```python
service = ImageGenerationService(
    db_host='localhost',
    db_user='root',
    db_password='password'
)
```

### Option 4: Mix and Match

```python
# Use config for most, override specific values
service = ImageGenerationService(
    db_host='different-host',  # Override
    use_config=True            # Use config for user/password
)
```

## 🔄 Migration Guide

### Old Code:
```python
from services.image_generation_service import ImageGenerationService

service = ImageGenerationService(
    db_host='localhost',
    db_user='root',
    db_password='password',
    db_name='PMP_Backend'
)
```

### New Code (Same - Backward Compatible):
```python
from services.image_generation_service import ImageGenerationService

service = ImageGenerationService(
    db_host='localhost',
    db_user='root',
    db_password='password',
    db_name='PMP_Backend'
)
```

### New Code (Using Config):
```python
from services.image_generation_service import ImageGenerationService

# No credentials needed - uses config/env
service = ImageGenerationService()
```

## ✅ Benefits

1. **Centralized Credential Management**
   - One place to manage database credentials
   - Integrates with existing config system

2. **Cleaner Code**
   - Context managers handle cleanup automatically
   - Less boilerplate code
   - Automatic transaction management

3. **More Flexible**
   - Multiple credential sources
   - Easy to switch between environments
   - Override specific values as needed

4. **Better Error Handling**
   - Automatic rollback on errors
   - Proper connection cleanup
   - Clear error messages

5. **Backward Compatible**
   - Existing code still works
   - No breaking changes
   - Gradual migration possible

## 🧪 Testing

Test the database service:
```bash
# Set environment variables
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=password

# Run tests
python backend/scripts/test_database_service.py
```

Test the image generation service:
```bash
# Dry run
python backend/scripts/generate_images.py --dry-run

# Process a few articles
python backend/scripts/generate_images.py --max-articles 5
```

## 📚 API Reference

### DatabaseService

**Constructor:**
```python
DatabaseService(
    host: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
    port: int = 3306,
    use_config: bool = True
)
```

**Methods:**
- `create_connection()` - Create a new connection
- `get_connection()` - Context manager for connections
- `get_cursor(dictionary=True)` - Context manager for cursors
- `test_connection()` - Test if connection works
- `get_connection_params()` - Get connection parameters dict

**Usage Examples:**
```python
# Get a connection
with db_service.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table")

# Get a cursor (preferred)
with db_service.get_cursor(dictionary=True) as cursor:
    cursor.execute("SELECT * FROM table")
    results = cursor.fetchall()

# Test connection
if db_service.test_connection():
    print("Connected!")
```

## 🎯 Next Steps

1. ✅ Database service created and integrated
2. ✅ Image generation service updated
3. ✅ Test script created
4. ⏭️ Test with your database
5. ⏭️ Run image generation

## 📝 Summary

The database service provides:
- ✅ Centralized credential management
- ✅ Integration with config system
- ✅ Cleaner, more maintainable code
- ✅ Better error handling
- ✅ Backward compatibility
- ✅ Flexible credential sources

**No breaking changes** - existing code continues to work!
