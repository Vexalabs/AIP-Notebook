# Auto-Update System Specification

## Executive Summary

This document outlines the current implementation and required improvements for the AIP Notebook auto-update system. The goal is to enable seamless, user-friendly updates where users are prompted when a new release is available on GitHub, and clicking the update button automatically pulls the latest version and restarts the application.

---

## Current Implementation Review

### ✅ What's Working

1. **Version Detection**
   - `VERSION` file at project root stores current version (currently `1.0.0`)
   - Backend reads version from `backend/routes/updates.py`
   - Frontend displays version in header

2. **Update Check API**
   - Endpoint: `GET /api/updates/check`
   - Queries GitHub API: `https://api.github.com/repos/Vexalabs/AIP-Notebook/releases/latest`
   - Compares current version with latest release tag
   - Returns update availability status and release info

3. **Frontend Update Banner**
   - Automatically checks for updates on app startup (in `App.jsx`)
   - Displays prominent banner when update is available
   - Shows new version number and "Update Now" button
   - Located at lines 268-287 in `frontend/src/App.jsx`

4. **Update Execution API**
   - Endpoint: `POST /api/updates/perform`
   - Downloads latest release asset (`AIP-Model-Builder-Installer.tar.gz`)
   - Generates bash script to apply update
   - Attempts to restart application

### ❌ Current Issues & Gaps

#### 1. **Platform Compatibility**
   - **Issue**: Update script is Linux/WSL-only (bash-based)
   - **Impact**: Won't work on native Windows or Mac installations
   - **Location**: `backend/routes/updates.py` lines 103-154

#### 2. **Git Pull Not Implemented**
   - **Issue**: Current implementation downloads release archive, doesn't use `git pull`
   - **Impact**: Doesn't leverage Git for version control
   - **User Expectation**: "pull the latest version from git"

#### 3. **Process Management**
   - **Issue**: Script kills processes (`pkill -f uvicorn`) which may terminate itself
   - **Impact**: Update may fail mid-execution
   - **Location**: Lines 133-135 in `updates.py`

#### 4. **No Rollback Mechanism**
   - **Issue**: If update fails, no way to revert to previous version
   - **Impact**: Could leave app in broken state

#### 5. **User Data Preservation**
   - **Current**: Uses `rsync` with exclusions for workspace, .secrets, venv
   - **Issue**: Not tested thoroughly, could overwrite user data
   - **Location**: Line 139 in `updates.py`

#### 6. **Frontend Hardcoded Version**
   - **Issue**: Version shown in UI is hardcoded (`v1.0.0` at line 264 in App.jsx)
   - **Impact**: Doesn't reflect actual installed version
   - **Should**: Fetch from backend API

#### 7. **No Update Progress Feedback**
   - **Issue**: User clicks "Update Now" and waits 10 seconds with minimal feedback
   - **Impact**: Poor UX, user doesn't know if it's working

#### 8. **Dependency Updates**
   - **Issue**: Script runs `./setup.sh` but may fail if dependencies change
   - **Impact**: App may not start after update

---

## Required Implementation

### Phase 1: Core Functionality (High Priority)

#### 1.1 Git-Based Update Mechanism

**Requirement**: Use `git pull` instead of downloading archives

**Implementation**:
```python
# backend/routes/updates.py

@router.post("/perform")
async def perform_update():
    """
    Pull latest code from git and restart application.
    """
    import subprocess
    import os
    from pathlib import Path
    
    app_dir = Path(__file__).parent.parent.parent.absolute()
    
    # Check if this is a git repository
    if not (app_dir / ".git").exists():
        raise HTTPException(
            status_code=400, 
            detail="This installation is not a git repository. Please reinstall from source."
        )
    
    # Create update script
    update_script = create_update_script(app_dir)
    
    # Execute update in background
    execute_update_script(update_script)
    
    return {"status": "success", "message": "Update initiated"}
```

**Update Script Template**:
```bash
#!/bin/bash
# Auto-generated update script

APP_DIR="{app_dir}"
LOG_FILE="$APP_DIR/update.log"

echo "Starting update process..." > "$LOG_FILE"

# Navigate to app directory
cd "$APP_DIR"

# Stash any local changes
git stash >> "$LOG_FILE" 2>&1

# Fetch latest changes
git fetch origin main >> "$LOG_FILE" 2>&1

# Pull latest code
git pull origin main >> "$LOG_FILE" 2>&1

# Update dependencies
echo "Updating backend dependencies..." >> "$LOG_FILE"
source venv/bin/activate
pip install -r backend/requirements.txt >> "$LOG_FILE" 2>&1

echo "Updating frontend dependencies..." >> "$LOG_FILE"
cd frontend
npm install >> "$LOG_FILE" 2>&1
npm run build >> "$LOG_FILE" 2>&1
cd ..

# Restart application
echo "Restarting application..." >> "$LOG_FILE"
pkill -f uvicorn
pkill -f vite

# Start services
nohup ./run.sh > /dev/null 2>&1 &

echo "Update complete!" >> "$LOG_FILE"
```

#### 1.2 Platform-Specific Update Scripts

**Windows (WSL)**:
```powershell
# update-windows.ps1
$AppDir = "\\wsl.localhost\Ubuntu\home\{user}\MLModelBuilder"

Write-Host "Stopping services..."
wsl -d Ubuntu bash -c "pkill -f uvicorn; pkill -f vite"

Write-Host "Pulling latest code..."
wsl -d Ubuntu bash -c "cd $AppDir && git pull origin main"

Write-Host "Updating dependencies..."
wsl -d Ubuntu bash -c "cd $AppDir && ./setup.sh"

Write-Host "Restarting application..."
wsl -d Ubuntu bash -c "cd $AppDir && nohup ./run.sh > /dev/null 2>&1 &"

Write-Host "Update complete!"
```

**Mac/Linux**:
```bash
# update-unix.sh
APP_DIR="{app_dir}"

echo "Stopping services..."
pkill -f uvicorn
pkill -f vite

echo "Pulling latest code..."
cd "$APP_DIR"
git pull origin main

echo "Updating dependencies..."
./setup.sh

echo "Restarting application..."
nohup ./run.sh > /dev/null 2>&1 &

echo "Update complete!"
```

#### 1.3 Dynamic Version Display

**Frontend Change**:
```javascript
// App.jsx
const [currentVersion, setCurrentVersion] = useState('...')

useEffect(() => {
    fetchCurrentVersion()
}, [])

const fetchCurrentVersion = async () => {
    try {
        const res = await axios.get('/api/updates/current-version')
        setCurrentVersion(res.data.version)
    } catch (err) {
        console.error("Failed to fetch version", err)
    }
}

// In render:
<div className="...">
    v{currentVersion}
</div>
```

#### 1.4 Update Progress Feedback

**Frontend Enhancement**:
```javascript
const [updateProgress, setUpdateProgress] = useState(null)

const performUpdate = async () => {
    if (!window.confirm("...")) return
    
    setLoading(true)
    setUpdateProgress("Initiating update...")
    
    try {
        await axios.post('/api/updates/perform')
        
        // Poll for update status
        const pollInterval = setInterval(async () => {
            try {
                const status = await axios.get('/api/updates/status')
                setUpdateProgress(status.data.message)
                
                if (status.data.complete) {
                    clearInterval(pollInterval)
                    setUpdateProgress("Update complete! Reloading...")
                    setTimeout(() => window.location.reload(), 2000)
                }
            } catch (err) {
                // Backend is down, update likely in progress
                setUpdateProgress("Applying update...")
            }
        }, 2000)
        
    } catch (err) {
        setUpdateProgress("Update failed: " + err.message)
        setLoading(false)
    }
}
```

**Backend Status Endpoint**:
```python
# backend/routes/updates.py

update_status = {"message": "Idle", "complete": False}

@router.get("/status")
async def get_update_status():
    """Get current update status."""
    return update_status

@router.post("/perform")
async def perform_update():
    global update_status
    update_status = {"message": "Starting update...", "complete": False}
    
    # ... rest of update logic
```

---

### Phase 2: Safety & Reliability (Medium Priority)

#### 2.1 Pre-Update Backup

**Implementation**:
```python
def create_backup(app_dir: Path) -> Path:
    """Create backup before updating."""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = app_dir.parent / f"AIP-Notebook-Backup-{timestamp}"
    
    # Copy critical files
    shutil.copytree(
        app_dir / "workspace",
        backup_dir / "workspace"
    )
    shutil.copytree(
        app_dir / ".secrets",
        backup_dir / ".secrets"
    )
    shutil.copy(
        app_dir / "VERSION",
        backup_dir / "VERSION"
    )
    
    return backup_dir
```

#### 2.2 Rollback Mechanism

**Implementation**:
```python
@router.post("/rollback")
async def rollback_update():
    """Rollback to previous version if update fails."""
    app_dir = Path(__file__).parent.parent.parent.absolute()
    
    # Find latest backup
    backups = sorted(app_dir.parent.glob("AIP-Notebook-Backup-*"))
    if not backups:
        raise HTTPException(status_code=404, detail="No backup found")
    
    latest_backup = backups[-1]
    
    # Restore from backup
    restore_script = f"""#!/bin/bash
    APP_DIR="{app_dir}"
    BACKUP_DIR="{latest_backup}"
    
    echo "Restoring from backup..."
    
    # Stop services
    pkill -f uvicorn
    pkill -f vite
    
    # Restore workspace and secrets
    rm -rf "$APP_DIR/workspace"
    rm -rf "$APP_DIR/.secrets"
    cp -r "$BACKUP_DIR/workspace" "$APP_DIR/"
    cp -r "$BACKUP_DIR/.secrets" "$APP_DIR/"
    
    # Checkout previous version
    cd "$APP_DIR"
    git checkout $(cat "$BACKUP_DIR/VERSION")
    
    # Restart
    nohup ./run.sh > /dev/null 2>&1 &
    
    echo "Rollback complete!"
    """
    
    # Execute rollback
    # ... (similar to update execution)
    
    return {"status": "success", "message": "Rollback initiated"}
```

#### 2.3 Update Validation

**Pre-Update Checks**:
```python
def validate_update_prerequisites() -> dict:
    """Check if system is ready for update."""
    checks = {
        "git_available": shutil.which("git") is not None,
        "git_repo": (app_dir / ".git").exists(),
        "no_uncommitted_changes": check_git_status(),
        "disk_space": check_disk_space(),
        "network_connection": check_github_connection()
    }
    
    return {
        "ready": all(checks.values()),
        "checks": checks
    }

@router.get("/validate")
async def validate_update():
    """Validate system is ready for update."""
    return validate_update_prerequisites()
```

---

### Phase 3: User Experience (Low Priority)

#### 3.1 Release Notes Display

**Frontend**:
```javascript
{updateAvailable && (
    <div className="...">
        <div>
            <h3>Update Available: v{updateInfo?.latest_version}</h3>
            <details>
                <summary>What's New</summary>
                <div className="prose">
                    {updateInfo?.release_notes}
                </div>
            </details>
        </div>
        <button onClick={performUpdate}>Update Now</button>
    </div>
)}
```

#### 3.2 Update Scheduling

**Allow users to schedule updates for later**:
```javascript
const [updateScheduled, setUpdateScheduled] = useState(false)

const scheduleUpdate = () => {
    localStorage.setItem('scheduled_update', updateInfo.latest_version)
    setUpdateScheduled(true)
    alert("Update will be applied next time you restart the application")
}
```

#### 3.3 Automatic Update Check Interval

**Backend**:
```python
# Check for updates every 24 hours
@router.get("/check")
async def check_for_updates(force: bool = False):
    """Check for updates with caching."""
    cache_file = app_dir / ".update_cache"
    
    if not force and cache_file.exists():
        cache_age = time.time() - cache_file.stat().st_mtime
        if cache_age < 86400:  # 24 hours
            return json.loads(cache_file.read_text())
    
    # Fetch from GitHub
    result = get_latest_version()
    
    # Cache result
    cache_file.write_text(json.dumps(result))
    
    return result
```

---

## Testing Plan

### Test Case 1: Fresh Installation to Update

1. Install v1.0.0 from release
2. Create v1.1.0 with visible changes (new sample model, theme change)
3. Push to GitHub and create release
4. Launch v1.0.0 app
5. Verify update banner appears
6. Click "Update Now"
7. Verify app updates and restarts
8. Verify new features are present
9. Verify workspace is preserved

### Test Case 2: Update Failure Recovery

1. Start update process
2. Simulate failure (kill process mid-update)
3. Verify app can recover or rollback
4. Verify user data is intact

### Test Case 3: No Internet Connection

1. Disconnect network
2. Launch app
3. Verify graceful handling of update check failure
4. Verify app still functions normally

### Test Case 4: Already Up-to-Date

1. Install latest version
2. Launch app
3. Verify no update banner appears
4. Verify version is correct

---

## File Changes Required

### New Files

1. `backend/routes/updates.py` - Enhanced update logic
2. `backend/scripts/update-unix.sh` - Unix update script template
3. `backend/scripts/update-windows.ps1` - Windows update script template
4. `frontend/src/components/UpdateBanner.jsx` - Dedicated update UI component

### Modified Files

1. `frontend/src/App.jsx`
   - Dynamic version fetching
   - Enhanced update progress UI
   - Update status polling

2. `backend/routes/updates.py`
   - Git-based update mechanism
   - Platform detection
   - Backup creation
   - Rollback support
   - Update validation

3. `VERSION`
   - Keep updated with each release

4. `README.md`
   - Document update process
   - Add troubleshooting section

---

## Implementation Priority

### Must Have (P0)
- ✅ Git pull-based updates
- ✅ Platform-specific scripts
- ✅ Dynamic version display
- ✅ Basic progress feedback

### Should Have (P1)
- ⚠️ Pre-update backup
- ⚠️ Update validation
- ⚠️ Better error handling

### Nice to Have (P2)
- 💡 Rollback mechanism
- 💡 Release notes display
- 💡 Update scheduling
- 💡 Automatic update checks

---

## Security Considerations

1. **Code Signing**: Future releases should be signed to verify authenticity
2. **HTTPS Only**: Always use HTTPS for GitHub API calls
3. **Permission Checks**: Verify write permissions before attempting update
4. **User Confirmation**: Always require explicit user consent before updating
5. **Backup User Data**: Never risk losing user workspace or configuration

---

## Success Criteria

The auto-update system is successful when:

1. ✅ User opens app and sees update banner within 5 seconds (if update available)
2. ✅ User clicks "Update Now" and update completes in < 2 minutes
3. ✅ App automatically restarts after update
4. ✅ User workspace and settings are preserved
5. ✅ New features from update are immediately available
6. ✅ Update works on Windows (WSL), Mac, and Linux
7. ✅ If update fails, app can recover to previous state
8. ✅ User receives clear feedback throughout update process

---

## Next Steps

1. **Review this specification** with stakeholders
2. **Prioritize features** based on user needs
3. **Implement Phase 1** (Core Functionality)
4. **Test thoroughly** on all platforms
5. **Create v1.1.0 release** to test update mechanism
6. **Iterate based on feedback**

---

## Appendix: Current Code Locations

- **Version File**: `VERSION` (root)
- **Backend Update Routes**: `backend/routes/updates.py`
- **Frontend Update Logic**: `frontend/src/App.jsx` (lines 20-21, 73-102, 268-287)
- **Package Creator**: `create-package.sh`
- **Launcher**: `start.bat`
- **Documentation**: `UPDATE_GUIDE.md`, `UPDATE_TESTING_GUIDE.md`
