import git
from pathlib import Path
import os
from typing import Optional

class GitService:
    def __init__(self):
        pass

    def clone_or_pull(self, repo_url: str, target_dir: str) -> git.Repo:
        """Clones the repo if not exists, otherwise pulls latest."""
        path = Path(target_dir)
        
        if path.exists() and (path / ".git").exists():
            repo = git.Repo(path)
            print(f"Repo exists at {target_dir}, pulling latest...")
            origin = repo.remotes.origin
            origin.pull()
            return repo
        else:
            print(f"Cloning {repo_url} to {target_dir}...")
            repo = git.Repo.clone_from(repo_url, target_dir)
            return repo

    def create_branch(self, repo: git.Repo, branch_name: str):
        """Creates and checks out a new branch."""
        current = repo.active_branch
        print(f"Current branch: {current.name}")
        
        # Create new branch from main
        if branch_name in repo.heads:
            print(f"Branch {branch_name} exists, checking out...")
            new_branch = repo.heads[branch_name]
        else:
            print(f"Creating new branch {branch_name}...")
            new_branch = repo.create_head(branch_name)
            
        new_branch.checkout()
        return new_branch

    def commit_and_push(self, repo: git.Repo, message: str, branch_name: str, token: str = None):
        """Stages all changes, commits, and pushes to remote."""
        if not repo.is_dirty(untracked_files=True):
            print("No changes to commit.")
            return

        print("Adding all files...")
        repo.git.add(A=True)
        
        print(f"Committing with message: {message}")
        repo.index.commit(message)
        
        print(f"Pushing to origin/{branch_name}...")
        origin = repo.remotes.origin
        
        # If token provided, temporarily set URL with authentication
        if token:
            from urllib.parse import quote
            original_url = list(origin.urls)[0]
            # Extract repo path from URL
            repo_path = original_url.replace("https://github.com/", "")
            # URL-encode the token to handle special characters
            encoded_token = quote(token, safe='')
            auth_url = f"https://{encoded_token}@github.com/{repo_path}"
            print(f"Setting authenticated URL for push...")
            origin.set_url(auth_url)  # Set globally, not just for push
        
        try:
            print(f"Pushing to {branch_name}...")
            push_infos = origin.push(branch_name, set_upstream=True)
            
            # Check for push errors
            for info in push_infos:
                if info.flags & (info.ERROR | info.REJECTED):
                    raise Exception(f"Push failed: {info.summary}")
                print(f"Push result: {info.summary}")
                
        except Exception as e:
            print(f"Git push exception: {e}")
            raise e
        finally:
            # Always restore original URL
            if token:
                print(f"Restoring original URL...")
                origin.set_url(original_url)

# Global instance
git_service = GitService()
