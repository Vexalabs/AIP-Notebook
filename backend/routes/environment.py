from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.jupyter_service import jupyter_service
import shutil
import traceback
from pathlib import Path

router = APIRouter(prefix="/api/environment", tags=["environment"])

class StartEnvRequest(BaseModel):
    template_id: str
    model_id: str

@router.post("/start")
async def start_environment(request: StartEnvRequest):
    """
    Starts the development environment (Jupyter).
    If a model_id is provided, it copies the sample model into a subdirectory of the workspace.
    """
    try:
        # Establish project root from the current file's location.
        # .../backend/routes/environment.py -> .../
        project_root = Path(__file__).parent.parent.parent
        workspace_dir = project_root / "workspace"
        launch_dir = workspace_dir
        
        if request.model_id and request.model_id != "default":
            import time
            start_time = time.time()
            
            sample_models_dir = project_root / "sample_models"
            source_dir = sample_models_dir / request.model_id
            destination_dir = workspace_dir / request.model_id
            launch_dir = destination_dir
            
            if not source_dir.exists() or not source_dir.is_dir():
                raise HTTPException(status_code=404, detail=f"Sample model '{request.model_id}' not found at '{source_dir}'.")
            
            # Only copy if destination doesn't exist (much faster on subsequent starts)
            if not destination_dir.exists():
                print(f"Copying sample model '{request.model_id}' to workspace...")
                shutil.copytree(source_dir, destination_dir)
                elapsed = time.time() - start_time
                print(f"Sample model copied in {elapsed:.2f} seconds")
            else:
                print(f"Sample model '{request.model_id}' already exists in workspace, skipping copy")

    except Exception as e:
        print(f"CRITICAL: Error copying sample model: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to copy sample model files: {e}")

    # Stop existing server if running to ensure we launch with new root
    if jupyter_service.is_running():
        jupyter_service.stop_server()

    result = jupyter_service.start_server(str(launch_dir))
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@router.post("/stop")
async def stop_environment():
    """Stops the development environment."""
    return jupyter_service.stop_server()

@router.get("/status")
async def get_status():
    """Gets the current status of the environment."""
    is_running = jupyter_service.is_running()
    return {
        "status": "running" if is_running else "stopped",
        "url": f"http://localhost:{jupyter_service.port}/tree?token={jupyter_service.token}" if is_running else None
    }
