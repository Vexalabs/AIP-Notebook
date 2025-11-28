from fastapi import APIRouter
from config import config

router = APIRouter(prefix="/api/debug", tags=["debug"])

@router.get("/config")
async def get_config_debug():
    """Debug endpoint to check current configuration"""
    return {
        "github_repo": config.github_repo,
        "github_token_present": bool(config.github_token),
        "github_token_length": len(config.github_token) if config.github_token else 0
    }
