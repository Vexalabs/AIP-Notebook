from fastapi import APIRouter, HTTPException
from pathlib import Path
import requests
from packaging import version as pkg_version

router = APIRouter(prefix="/api/updates", tags=["updates"])

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
    """Fetch latest release info from GitHub."""
    try:
        # Check GitHub releases for latest version
        # Replace with your actual repository
        api_url = "https://api.github.com/repos/Vexalabs/AIP-Notebook/releases/latest"
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "version": data.get("tag_name", "").lstrip("v"),
                "url": data.get("html_url"),
                "download_url": data.get("zipball_url"),
                "notes": data.get("body", "")
            }
    except Exception as e:
        print(f"Error fetching latest version: {e}")
    
    return {"version": "0.0.0", "url": None}

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

@router.post("/perform")
async def perform_update():
    """
    Automatically download and apply the latest update.
    """
    latest_info = get_latest_version()
    download_url = latest_info.get("download_url") # GitHub zipball/tarball url
    # Ideally we want the specific asset url (our installer tar.gz), not the source code zip
    # But for now let's assume the release has the asset we want.
    # We need to find the asset named 'MLModelBuilder-Installer.tar.gz' in the assets list.
    
    # Fetch release info again to get assets
    try:
        api_url = "https://api.github.com/repos/Vexalabs/AIP-Notebook/releases/latest"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            assets = data.get("assets", [])
            for asset in assets:
                if asset["name"] == "AIP-Model-Builder-Installer.tar.gz":
                    download_url = asset["browser_download_url"]
                    break
    except Exception as e:
        print(f"Error finding asset: {e}")

    if not download_url:
        raise HTTPException(status_code=404, detail="Update package not found in latest release")

    import subprocess
    import os
    import tempfile

    # Define paths
    # We assume we are running in ~/MLModelBuilder/backend
    # We want to update ~/MLModelBuilder
    app_dir = Path(__file__).parent.parent.parent.absolute() # ~/MLModelBuilder
    
    # Create the update script
    update_script_content = f"""#!/bin/bash
# Auto-generated update script
APP_DIR="{app_dir}"
URL="{download_url}"
TEMP_DIR=$(mktemp -d)
ARCHIVE="$TEMP_DIR/update.tar.gz"

echo "Starting Update Process..."
echo "Downloading update from $URL..."

# Download
curl -L -o "$ARCHIVE" "$URL"

if [ ! -f "$ARCHIVE" ]; then
    echo "Download failed."
    exit 1
fi

echo "Extracting..."
tar -xzf "$ARCHIVE" -C "$TEMP_DIR"

# The archive contains a folder 'AIP-Model-Builder-Installer'
SOURCE_DIR="$TEMP_DIR/AIP-Model-Builder-Installer/MLModelBuilder"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Invalid archive structure."
    exit 1
fi

echo "Stopping services..."
pkill -f uvicorn
pkill -f vite
pkill -f jupyter

echo "Applying updates..."
# Copy files over, excluding user data
rsync -av --exclude 'workspace' --exclude '.secrets' --exclude 'venv' --exclude 'node_modules' "$SOURCE_DIR/" "$APP_DIR/"

echo "Updating dependencies..."
cd "$APP_DIR"
# We can try to update venv, but it might be locked if python is running this script?
# Actually this script is running via bash, so python is gone (killed above).
# But wait, if we kill python (uvicorn), this script might die if it was a child?
# We must run this script with nohup and disown.

./setup.sh

echo "Restarting application..."
nohup ./run.sh > /dev/null 2>&1 &

echo "Update Complete!"
"""
    
    update_script_path = app_dir / "apply_update.sh"
    update_script_path.write_text(update_script_content)
    
    # Make executable
    os.chmod(update_script_path, 0o755)
    
    # Execute in background and detach
    # We use nohup to ensure it survives when we kill the parent process
    subprocess.Popen(
        ["nohup", str(update_script_path)],
        cwd=str(app_dir),
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    return {"status": "success", "message": "Update started. Application will restart shortly."}

