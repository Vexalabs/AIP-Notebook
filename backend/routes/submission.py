from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.git_service import git_service
from services.github_service import github_service
from config import config
import os
import time
import git
import tempfile
import shutil

router = APIRouter(prefix="/api/submission", tags=["submission"])

class SubmitModelRequest(BaseModel):
    commit_message: str
    description: str

@router.post("/submit")
async def submit_model(request: SubmitModelRequest):
    """
    Submits the current model code by creating a PR.
    """
    if not config.github_token:
        raise HTTPException(status_code=400, detail="GitHub token not configured")

    # Workspace dir - find it relative to the backend directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    workspace_dir = os.path.join(project_root, "workspace")
    
    # Verify workspace exists
    if not os.path.exists(workspace_dir):
        raise HTTPException(status_code=500, detail=f"Workspace directory not found at {workspace_dir}")
    
    # Temp dir for git operations
    temp_dir = tempfile.mkdtemp(prefix="model_submission_")
    
    try:
        # 1. Clone repo to temp directory
        print(f"Cloning repo to {temp_dir}...")
        repo_url = "https://github.com/Vexalabs/AI-Predictions-Model-Templates.git"
        repo = git.Repo.clone_from(repo_url, temp_dir)
        
        # 2. Copy user files from workspace to temp dir
        print(f"Copying user files from {workspace_dir}...")
        for item in os.listdir(workspace_dir):
            src = os.path.join(workspace_dir, item)
            dst = os.path.join(temp_dir, item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src) and item not in ['.git', '.ipynb_checkpoints']:
                shutil.copytree(src, dst, dirs_exist_ok=True)
        
        # 3. Create new branch
        timestamp = int(time.time())
        branch_name = f"model-submission-{timestamp}"
        git_service.create_branch(repo, branch_name)
        
        # 4. Commit and Push
        print(f"Pushing branch {branch_name}...")
        git_service.commit_and_push(repo, request.commit_message, branch_name, config.github_token)
        
        # 5. Wait for GitHub to register the branch
        print("Waiting for GitHub to register branch...")
        max_retries = 10
        for i in range(max_retries):
            if github_service.verify_branch(branch_name):
                print(f"Branch {branch_name} verified on GitHub.")
                break
            print(f"Branch not ready yet, retrying ({i+1}/{max_retries})...")
            time.sleep(2)
        else:
            print("WARNING: Branch verification timed out. Attempting PR creation anyway...")
        
        # 6. Create PR
        print(f"Creating PR for branch {branch_name}...")
        pr_url = github_service.create_pr(
            title=f"Model Submission: {request.commit_message}",
            body=request.description,
            head_branch=branch_name,
            base_branch="main"
        )
        
        # 7. Auto-star the repo (if not already starred)
        try:
            github_service.auto_star_repo()
        except Exception as e:
            print(f"Auto-star failed (non-critical): {e}")
        
        return {"status": "success", "pr_url": pr_url}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Submission failed: {str(e)}")
    finally:
        # Clean up temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
