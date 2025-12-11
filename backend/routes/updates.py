from fastapi import APIRouter, HTTPException
from pathlib import Path
import requests
from packaging import version as pkg_version
import subprocess
import os
import shutil
import platform
import time
import json
from datetime import datetime

router = APIRouter(prefix="/api/updates", tags=["updates"])

# Global update status for progress tracking
update_status = {"message": "Idle", "complete": False, "error": None}

def get_current_version() -> str:
    """Read current version from VERSION file."""
    try:
        version_file = Path(__file__).parent.parent.parent / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "0.0.0"
    except Exception as e:
        print(f"Error reading version: {e}")
        return "0.0.0"

def get_latest_version() -> dict:
    """Fetch latest release info from GitHub with caching."""
    app_dir = Path(__file__).parent.parent.parent
    cache_file = app_dir / ".update_cache"
    
    # Check cache (5 minute TTL)
    if cache_file.exists():
        cache_age = time.time() - cache_file.stat().st_mtime
        if cache_age < 300:  # 5 minutes
            try:
                return json.loads(cache_file.read_text())
            except:
                pass
    
    try:
        api_url = "https://api.github.com/repos/Vexalabs/AIP-Notebook/releases/latest"
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            result = {
                "version": data.get("tag_name", "").lstrip("v"),
                "url": data.get("html_url"),
                "download_url": data.get("zipball_url"),
                "notes": data.get("body", "")
            }
            
            # Cache the result
            try:
                cache_file.write_text(json.dumps(result))
            except:
                pass
            
            return result
    except Exception as e:
        print(f"Error fetching latest version: {e}")
    
    return {"version": "0.0.0", "url": None}

def detect_platform() -> str:
    """Detect the current platform."""
    system = platform.system().lower()
    if system == "linux":
        # Check if running in WSL
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    return "wsl"
        except:
            pass
        return "linux"
    elif system == "darwin":
        return "mac"
    elif system == "windows":
        return "windows"
    return "unknown"

def validate_update_prerequisites() -> dict:
    """Validate system is ready for update."""
    app_dir = Path(__file__).parent.parent.parent
    
    checks = {
        "git_available": shutil.which("git") is not None,
        "git_repo": (app_dir / ".git").exists(),
        "disk_space": check_disk_space(app_dir),
        "network_connection": check_github_connection()
    }
    
    # Check for uncommitted changes
    if checks["git_repo"] and checks["git_available"]:
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(app_dir),
                capture_output=True,
                text=True,
                timeout=5
            )
            checks["no_uncommitted_changes"] = len(result.stdout.strip()) == 0
        except:
            checks["no_uncommitted_changes"] = False
    else:
        checks["no_uncommitted_changes"] = True
    
    return {
        "ready": all(checks.values()),
        "checks": checks
    }

def check_disk_space(path: Path) -> bool:
    """Check if there's enough disk space (>500MB)."""
    try:
        stat = shutil.disk_usage(path)
        free_mb = stat.free / (1024 * 1024)
        return free_mb > 500
    except:
        return True  # Assume OK if we can't check

def check_github_connection() -> bool:
    """Check if GitHub is reachable."""
    try:
        response = requests.get("https://api.github.com", timeout=3)
        return response.status_code == 200
    except:
        return False

def create_backup(app_dir: Path) -> Path:
    """Create backup of critical files before update."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = app_dir.parent / f"AIP-Notebook-Backup-{timestamp}"
    
    try:
        backup_dir.mkdir(exist_ok=True)
        
        # Backup workspace
        if (app_dir / "workspace").exists():
            shutil.copytree(
                app_dir / "workspace",
                backup_dir / "workspace",
                dirs_exist_ok=True
            )
        
        # Backup .secrets
        if (app_dir / ".secrets").exists():
            shutil.copytree(
                app_dir / ".secrets",
                backup_dir / ".secrets",
                dirs_exist_ok=True
            )
        
        # Backup VERSION
        if (app_dir / "VERSION").exists():
            shutil.copy(
                app_dir / "VERSION",
                backup_dir / "VERSION"
            )
        
        return backup_dir
    except Exception as e:
        print(f"Backup failed: {e}")
        raise

def generate_update_script(app_dir: Path, platform_type: str) -> str:
    """Generate platform-specific update script."""
    
    if platform_type in ["linux", "wsl", "mac"]:
        # Unix-based update script
        return f"""#!/bin/bash
# Auto-generated update script
APP_DIR="{app_dir}"
LOG_FILE="$APP_DIR/update.log"

echo "Starting update process..." > "$LOG_FILE"
echo "Timestamp: $(date)" >> "$LOG_FILE"

# Navigate to app directory
cd "$APP_DIR" || exit 1

# Stash any local changes (just in case)
echo "Stashing local changes..." >> "$LOG_FILE"
git stash >> "$LOG_FILE" 2>&1

# Fetch latest changes
echo "Fetching latest code..." >> "$LOG_FILE"
git fetch origin main >> "$LOG_FILE" 2>&1

# Pull latest code
echo "Pulling latest code..." >> "$LOG_FILE"
git pull origin main >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "Git pull failed!" >> "$LOG_FILE"
    exit 1
fi

# Update backend dependencies
echo "Updating backend dependencies..." >> "$LOG_FILE"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    pip install -r backend/requirements.txt >> "$LOG_FILE" 2>&1
fi

# Update frontend dependencies and build
echo "Updating frontend..." >> "$LOG_FILE"
if [ -d "frontend" ]; then
    cd frontend
    npm install >> "$LOG_FILE" 2>&1
    npm run build >> "$LOG_FILE" 2>&1
    cd ..
fi

# Stop services
echo "Stopping services..." >> "$LOG_FILE"
pkill -f uvicorn
pkill -f vite
sleep 2

# Restart application
echo "Restarting application..." >> "$LOG_FILE"
nohup ./run.sh >> "$LOG_FILE" 2>&1 &

echo "Update complete!" >> "$LOG_FILE"
echo "Timestamp: $(date)" >> "$LOG_FILE"
"""
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Platform '{platform_type}' not supported for auto-update"
        )

@router.get("/check")
async def check_for_updates():
    """Check if a newer version is available."""
    current = get_current_version()
    latest_info = get_latest_version()
    latest = latest_info.get("version", "0.0.0")
    
    try:
        is_update_available = pkg_version.parse(latest) > pkg_version.parse(current)
    except Exception:
        is_update_available = False
    
    return {
        "current_version": current,
        "latest_version": latest,
        "update_available": is_update_available,
        "download_url": latest_info.get("url"),
        "release_notes": latest_info.get("notes", "")
    }

@router.get("/current-version")
async def current_version():
    """Get the current installed version."""
    return {"version": get_current_version()}

@router.get("/validate")
async def validate_update():
    """Validate system is ready for update."""
    return validate_update_prerequisites()

@router.get("/status")
async def get_update_status():
    """Get current update status."""
    return update_status

@router.post("/perform")
async def perform_update():
    """
    Update application using Git (development) or archive (production).
    Automatically detects installation type.
    """
    global update_status
    
    app_dir = Path(__file__).parent.parent.parent.absolute()
    
    # Reset status
    update_status = {"message": "Validating prerequisites...", "complete": False, "error": None}
    
    # Detect installation type
    is_git_repo = (app_dir / ".git").exists()
    
    if is_git_repo:
        # Development installation - use Git-based update
        return await perform_git_update(app_dir)
    else:
        # Production installation - use archive-based update
        return await perform_archive_update(app_dir)

async def perform_git_update(app_dir: Path):
    """Git-based update for development installations."""
    global update_status
    
    update_status["message"] = "Validating Git repository..."
    
    # Validate prerequisites
    validation = validate_update_prerequisites()
    if not validation["ready"]:
        failed_checks = [k for k, v in validation["checks"].items() if not v]
        update_status["error"] = f"Prerequisites not met: {', '.join(failed_checks)}"
        raise HTTPException(
            status_code=400,
            detail=f"Prerequisites not met: {', '.join(failed_checks)}"
        )
    
    # Detect platform
    platform_type = detect_platform()
    if platform_type == "unknown":
        update_status["error"] = "Unknown platform"
        raise HTTPException(
            status_code=400,
            detail="Could not detect platform"
        )
    
    try:
        # Create backup
        update_status["message"] = "Creating backup..."
        backup_dir = create_backup(app_dir)
        
        # Generate update script
        update_status["message"] = "Preparing update..."
        script_content = generate_update_script(app_dir, platform_type)
        
        # Write script
        script_path = app_dir / "apply_update.sh"
        script_path.write_text(script_content)
        os.chmod(script_path, 0o755)
        
        # Execute update script in background
        update_status["message"] = "Starting update..."
        subprocess.Popen(
            ["nohup", str(script_path)],
            cwd=str(app_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        # Mark as in progress
        update_status["message"] = "Update in progress..."
        
        return {
            "status": "success",
            "message": "Git-based update initiated. Application will restart shortly.",
            "backup_location": str(backup_dir),
            "update_type": "git"
        }
        
    except Exception as e:
        update_status["error"] = str(e)
        update_status["complete"] = True
        raise HTTPException(status_code=500, detail=str(e))

async def perform_archive_update(app_dir: Path):
    """Archive-based update for production installations."""
    global update_status
    
    update_status["message"] = "Fetching latest release..."
    
    # Get latest release info
    latest_info = get_latest_version()
    
    # Check if there's a newer version available
    current_version = get_current_version()
    latest_version = latest_info.get("version", "0.0.0")
    
    try:
        is_newer = pkg_version.parse(latest_version) > pkg_version.parse(current_version)
    except:
        is_newer = False
    
    if not is_newer:
        update_status["message"] = "Already up to date"
        update_status["complete"] = True
        raise HTTPException(
            status_code=400,
            detail=f"Already running latest version ({current_version})"
        )
    
    # Find installer asset
    download_url = None
    try:
        api_url = "https://api.github.com/repos/Vexalabs/AIP-Notebook/releases/latest"
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 404:
            # No releases published yet
            update_status["error"] = "No releases available"
            raise HTTPException(
                status_code=404,
                detail="No releases have been published yet. Please create a GitHub release with the installer package to enable updates."
            )
        
        if response.status_code == 200:
            data = response.json()
            assets = data.get("assets", [])
            
            # Look for installer package
            for asset in assets:
                if asset["name"] == "AIP-Model-Builder-Installer.tar.gz":
                    download_url = asset["browser_download_url"]
                    break
            
            if not download_url:
                # Release exists but no installer attached
                update_status["error"] = "Installer package not found"
                
                # Provide helpful error message
                available_assets = [a["name"] for a in assets] if assets else []
                if available_assets:
                    detail = f"Release v{latest_version} exists but installer package 'AIP-Model-Builder-Installer.tar.gz' is not attached. Available assets: {', '.join(available_assets)}"
                else:
                    detail = f"Release v{latest_version} exists but has no assets attached. Please upload 'AIP-Model-Builder-Installer.tar.gz' to the release."
                
                raise HTTPException(status_code=404, detail=detail)
        else:
            # Other error
            update_status["error"] = f"GitHub API error: {response.status_code}"
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch release info from GitHub (status {response.status_code})"
            )
            
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except Exception as e:
        update_status["error"] = str(e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch release: {str(e)}")
    
    # Detect platform
    platform_type = detect_platform()
    if platform_type == "unknown":
        update_status["error"] = "Unknown platform"
        raise HTTPException(status_code=400, detail="Could not detect platform")
    
    try:
        # Create backup
        update_status["message"] = "Creating backup..."
        backup_dir = create_backup(app_dir)
        
        # Generate archive-based update script
        update_status["message"] = "Preparing update..."
        script_content = generate_archive_update_script(app_dir, download_url, platform_type)
        
        # Write script
        script_path = app_dir / "apply_update.sh"
        script_path.write_text(script_content)
        os.chmod(script_path, 0o755)
        
        # Execute update script in background
        update_status["message"] = "Starting update..."
        subprocess.Popen(
            ["nohup", str(script_path)],
            cwd=str(app_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        # Mark as in progress
        update_status["message"] = "Update in progress..."
        
        return {
            "status": "success",
            "message": "Archive-based update initiated. Application will restart shortly.",
            "backup_location": str(backup_dir),
            "update_type": "archive"
        }
        
    except Exception as e:
        update_status["error"] = str(e)
        update_status["complete"] = True
        raise HTTPException(status_code=500, detail=str(e))

def generate_archive_update_script(app_dir: Path, download_url: str, platform_type: str) -> str:
    """Generate archive-based update script for production installations."""
    
    if platform_type in ["linux", "wsl", "mac"]:
        return f"""#!/bin/bash
# Auto-generated archive update script
APP_DIR="{app_dir}"
URL="{download_url}"
LOG_FILE="$APP_DIR/update.log"
TEMP_DIR=$(mktemp -d)
ARCHIVE="$TEMP_DIR/update.tar.gz"

echo "Starting archive-based update..." > "$LOG_FILE"
echo "Timestamp: $(date)" >> "$LOG_FILE"

# Download update
echo "Downloading update from $URL..." >> "$LOG_FILE"
curl -L -o "$ARCHIVE" "$URL" >> "$LOG_FILE" 2>&1

if [ ! -f "$ARCHIVE" ]; then
    echo "Download failed!" >> "$LOG_FILE"
    exit 1
fi

# Extract archive
echo "Extracting archive..." >> "$LOG_FILE"
tar -xzf "$ARCHIVE" -C "$TEMP_DIR" >> "$LOG_FILE" 2>&1

# Find source directory
SOURCE_DIR="$TEMP_DIR/AIP-Model-Builder-Installer/AIP-Model-Builder"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Invalid archive structure!" >> "$LOG_FILE"
    exit 1
fi

# Stop services
echo "Stopping services..." >> "$LOG_FILE"
pkill -f uvicorn
pkill -f vite
sleep 2

# Apply updates (preserve workspace and .secrets)
echo "Applying updates..." >> "$LOG_FILE"
rsync -av --exclude 'workspace' --exclude '.secrets' --exclude 'venv' --exclude 'node_modules' "$SOURCE_DIR/" "$APP_DIR/" >> "$LOG_FILE" 2>&1

# Update dependencies
echo "Updating dependencies..." >> "$LOG_FILE"
cd "$APP_DIR"

# Backend dependencies
if [ -f "backend/requirements.txt" ]; then
    if [ -d "backend/venv" ]; then
        source backend/venv/bin/activate
        pip install -r backend/requirements.txt >> "$LOG_FILE" 2>&1
    fi
fi

# Frontend dependencies
if [ -d "frontend" ]; then
    cd frontend
    npm install >> "$LOG_FILE" 2>&1
    npm run build >> "$LOG_FILE" 2>&1
    cd ..
fi

# Restart application
echo "Restarting application..." >> "$LOG_FILE"
nohup ./run.sh >> "$LOG_FILE" 2>&1 &

echo "Update complete!" >> "$LOG_FILE"
echo "Timestamp: $(date)" >> "$LOG_FILE"

# Cleanup
rm -rf "$TEMP_DIR"
"""
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Platform '{platform_type}' not supported for auto-update"
        )


@router.post("/rollback")
async def rollback_update():
    """Rollback to previous version if update fails."""
    app_dir = Path(__file__).parent.parent.parent.absolute()
    
    # Find latest backup
    backups = sorted(app_dir.parent.glob("AIP-Notebook-Backup-*"))
    if not backups:
        raise HTTPException(status_code=404, detail="No backup found")
    
    latest_backup = backups[-1]
    
    try:
        # Stop services
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        subprocess.run(["pkill", "-f", "vite"], check=False)
        time.sleep(2)
        
        # Restore workspace
        if (latest_backup / "workspace").exists():
            if (app_dir / "workspace").exists():
                shutil.rmtree(app_dir / "workspace")
            shutil.copytree(latest_backup / "workspace", app_dir / "workspace")
        
        # Restore .secrets
        if (latest_backup / ".secrets").exists():
            if (app_dir / ".secrets").exists():
                shutil.rmtree(app_dir / ".secrets")
            shutil.copytree(latest_backup / ".secrets", app_dir / ".secrets")
        
        # Checkout previous version
        if (latest_backup / "VERSION").exists():
            old_version = (latest_backup / "VERSION").read_text().strip()
            subprocess.run(
                ["git", "checkout", f"v{old_version}"],
                cwd=str(app_dir),
                check=True
            )
        
        # Restart services
        subprocess.Popen(
            ["nohup", "./run.sh"],
            cwd=str(app_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        return {
            "status": "success",
            "message": "Rollback complete. Application restarting.",
            "restored_from": str(latest_backup)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rollback failed: {str(e)}")
