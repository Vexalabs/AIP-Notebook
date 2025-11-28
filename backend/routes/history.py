from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.github_service import github_service
import os
import shutil
import time
import git
from pathlib import Path
import tempfile

router = APIRouter(prefix="/api/history", tags=["history"])

class RestoreRequest(BaseModel):
    sha: str
    branch: str

@router.get("/submissions")
async def list_submissions():
    """List all submissions (PRs) made by the user."""
    return github_service.get_user_submissions()

@router.post("/restore")
async def restore_submission(request: RestoreRequest):
    """
    Restores the workspace to the state of a previous submission.
    """
    try:
        # Define paths
        backend_dir = Path(__file__).parent.parent.absolute()
        project_root = backend_dir.parent
        workspace_dir = project_root / "workspace"
        
        # 1. Create Backup of current workspace
        timestamp = int(time.time())
        backup_dir = project_root / f"workspace_backup_{timestamp}"
        
        if workspace_dir.exists():
            print(f"Backing up workspace to {backup_dir}...")
            shutil.copytree(workspace_dir, backup_dir)
        else:
            workspace_dir.mkdir(parents=True, exist_ok=True)
            
        # 2. Clone repo to temp dir
        temp_dir = tempfile.mkdtemp(prefix="restore_")
        
        try:
            print(f"Cloning repo to {temp_dir}...")
            # We need the repo URL. Since we are restoring from the templates repo:
            repo_url = "https://github.com/Vexalabs/AI-Predictions-Model-Templates.git"
            
            repo = git.Repo.clone_from(repo_url, temp_dir)
            
            # Try multiple strategies to get the code
            print(f"Attempting to restore from branch: {request.branch}")
            
            try:
                # Strategy 1: Try to fetch and checkout the branch directly
                print(f"Fetching branch {request.branch}...")
                repo.git.fetch("origin", f"{request.branch}:{request.branch}")
                repo.git.checkout(request.branch)
                print(f"Successfully checked out branch {request.branch}")
            except git.exc.GitCommandError as e1:
                print(f"Branch checkout failed: {e1}")
                
                try:
                    # Strategy 2: Try to fetch from PR refs (for open PRs)
                    # GitHub stores PR branches as refs/pull/{pr_number}/head
                    # We need to extract PR number from the branch or try fetching all PRs
                    print("Fetching all PR refs...")
                    repo.git.fetch("origin", "+refs/pull/*/head:refs/remotes/origin/pr/*")
                    
                    # Now try to find and checkout our SHA
                    print(f"Checking out SHA {request.sha}...")
                    repo.git.checkout(request.sha)
                    print(f"Successfully checked out SHA {request.sha}")
                except git.exc.GitCommandError as e2:
                    print(f"PR refs checkout failed: {e2}")
                    
                    # Strategy 3: Last resort - try direct SHA fetch (GitHub allows this)
                    print(f"Attempting direct SHA fetch...")
                    repo.git.fetch("origin", request.sha)
                    repo.git.checkout(request.sha)
                    print(f"Successfully checked out SHA {request.sha}")
            
            # 4. Replace workspace content
            print("Restoring files...")
            
            # Clear current workspace (except hidden files if we want, but usually we want a clean slate)
            # We'll keep .ipynb_checkpoints just in case
            for item in os.listdir(workspace_dir):
                if item == '.ipynb_checkpoints': continue
                item_path = workspace_dir / item
                if item_path.is_file():
                    item_path.unlink()
                elif item_path.is_dir():
                    shutil.rmtree(item_path)
                    
            # Copy files from temp dir to workspace
            # We exclude .git folder
            for item in os.listdir(temp_dir):
                if item == '.git': continue
                
                src = Path(temp_dir) / item
                dst = workspace_dir / item
                
                if src.is_file():
                    shutil.copy2(src, dst)
                elif src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                    
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        return {
            "status": "success", 
            "message": "Workspace restored successfully",
            "backup_path": str(backup_dir)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")
