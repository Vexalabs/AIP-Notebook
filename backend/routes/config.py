from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from pathlib import Path
from config import config

router = APIRouter(prefix="/api/config", tags=["config"])

class TokenSaveRequest(BaseModel):
    token: str
    username: str

@router.post("/save-token")
async def save_github_token(request: TokenSaveRequest):
    """
    Saves the GitHub token to the config file.
    """
    try:
        # Get config path
        base_dir = Path(__file__).parent.parent.parent
        secrets_dir = base_dir / ".secrets"
        config_path = secrets_dir / "config.json"
        
        # Ensure .secrets directory exists
        secrets_dir.mkdir(exist_ok=True)
        
        # Load existing config or create new one
        if config_path.exists():
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        else:
            config_data = {
                "gcp": {
                    "project_id": "",
                    "region": "us-central1"
                },
                "github": {
                    "repo_owner": "Vexalabs",
                    "repo_name": "AIP-Notebook"
                }
            }
        
        # Update GitHub token
        if "github" not in config_data:
            config_data["github"] = {}
        
        config_data["github"]["token"] = request.token
        config_data["github"]["repo_owner"] = "Vexalabs"
        config_data["github"]["repo_name"] = "AI-Predictions-Model-Templates"
        
        # Save config
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
            
        return {"message": "Token saved successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save token: {e}")
        
@router.get("/check-setup")
async def get_config_status():
    """
    Checks the configuration status, including if the GitHub token is set.
    """
    try:
        base_dir = Path(__file__).parent.parent.parent
        config_path = base_dir / ".secrets" / "config.json"
        
        if not config_path.exists():
            return {"setup_complete": False, "has_github_token": False}
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Check if GitHub token exists
        has_token = (
            "github" in config_data and 
            "token" in config_data["github"] and 
            config_data["github"]["token"]
        )
        
        return {
            "setup_complete": has_token,
            "has_github_token": has_token
        }
        
    except Exception as e:
        return {"setup_complete": False, "has_github_token": False, "error": str(e)}
