from github import Github
from config import config
from typing import Optional
import time

class GitHubService:
    def __init__(self):
        self.client = None
    
    def _ensure_client(self):
        """Initialize the GitHub client if not already done."""
        if self.client is None and config.github_token:
            self.client = Github(config.github_token)
        return self.client

    def get_username(self) -> Optional[str]:
        """Get the authenticated user's username."""
        client = self._ensure_client()
        if not client:
            return None
        try:
            user = client.get_user()
            return user.login
        except Exception as e:
            print(f"Failed to get username: {e}")
            return None

    def ensure_fork(self, upstream_repo: str) -> Optional[str]:
        """
        Ensures the user has a fork of the upstream repository.
        Returns the clone URL of the fork with authentication.
        """
        client = self._ensure_client()
        if not client:
            return None
        
        try:
            user = client.get_user()
            upstream = client.get_repo(upstream_repo)
            repo_name = upstream_repo.split('/')[1]
            
            # Check if fork already exists
            try:
                fork = user.get_repo(repo_name)
                print(f"Fork already exists: {fork.full_name}")
            except:
                # Fork doesn't exist, create it
                print(f"Creating fork of {upstream_repo}...")
                fork = user.create_fork(upstream)
                # Wait a moment for fork to be ready
                time.sleep(3)
            
            # Return authenticated clone URL
            from urllib.parse import quote
            token = config.github_token
            encoded_token = quote(token, safe='')
            return f"https://{encoded_token}@github.com/{fork.full_name}.git"
            
        except Exception as e:
            print(f"Failed to ensure fork: {e}")
            return None

    def verify_branch_in_fork(self, username: str, repo_name: str, branch_name: str) -> bool:
        """Checks if a branch exists in the user's fork."""
        client = self._ensure_client()
        if not client:
            return False
            
        try:
            repo = client.get_repo(f"{username}/{repo_name}")
            repo.get_branch(branch_name)
            return True
        except Exception:
            return False

    def verify_branch(self, branch_name: str) -> bool:
        """Checks if a branch exists in the repo."""
        client = self._ensure_client()
        if not client:
            return False
            
        try:
            repo_name = config.github_repo
            repo = client.get_repo(repo_name)
            repo.get_branch(branch_name)
            return True
        except Exception:
            return False

    def create_pr_from_fork(self, title: str, body: str, head_branch: str, base_branch: str, upstream_repo: str) -> Optional[str]:
        """
        Creates a Pull Request from a fork to the upstream repository.
        head_branch should be in format: "username:branch_name"
        """
        client = self._ensure_client()
        
        if not client:
            print("GitHub client not initialized (no token).")
            return None

        try:
            repo = client.get_repo(upstream_repo)
            
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,  # Format: username:branch
                base=base_branch
            )
            
            print(f"PR created successfully: {pr.html_url}")
            return pr.html_url
            
        except Exception as e:
            print(f"Failed to create PR from fork: {e}")
            raise e

    def create_pr(self, title: str, body: str, head_branch: str, base_branch: str = "main") -> Optional[str]:
        """
        Creates a Pull Request on GitHub.
        Returns the URL of the created PR.
        """
        # Ensure client is initialized with current token
        client = self._ensure_client()
        
        if not client:
            print("GitHub client not initialized (no token).")
            return None

        repo_name = config.github_repo
        if not repo_name:
            print("GitHub repo not configured.")
            return None

        try:
            repo = client.get_repo(repo_name)
            
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            
            print(f"PR created successfully: {pr.html_url}")
            return pr.html_url
            
        except Exception as e:
            print(f"Failed to create PR: {e}")
            raise e
    
    def auto_star_repo(self) -> bool:
        """
        Automatically stars the repository if not already starred.
        Returns True if star was added, False if already starred or failed.
        """
        client = self._ensure_client()
        
        if not client:
            return False
        
        repo_name = config.github_repo
        if not repo_name:
            return False
        
        try:
            # Get the authenticated user
            user = client.get_user()
            
            # Get the repository
            repo = client.get_repo(repo_name)
            
            # Check if already starred
            if user.has_in_starred(repo):
                print(f"Repository {repo_name} is already starred ⭐")
                return False
            
            # Star the repository
            user.add_to_starred(repo)
            print(f"✨ Automatically starred repository: {repo_name}")
            return True
            
        except Exception as e:
            # Silently fail - don't interrupt user workflow
            print(f"Note: Could not auto-star repo (this is okay): {e}")
            return False

    def get_user_submissions(self):
        """
        Fetches list of PRs created by the current user.
        """
        client = self._ensure_client()
        if not client: return []
        
        repo_name = config.github_repo
        if not repo_name: return []
        
        try:
            user = client.get_user()
            # Search for PRs by this user in this repo
            query = f"repo:{repo_name} is:pr author:{user.login}"
            issues = client.search_issues(query, sort="created", order="desc")
            
            results = []
            for issue in issues:
                # We need to get the PR object to get the head sha/ref
                pr = issue.as_pull_request()
                results.append({
                    "id": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "created_at": pr.created_at.isoformat(),
                    "html_url": pr.html_url,
                    "branch": pr.head.ref,
                    "sha": pr.head.sha,
                    "merged": pr.merged
                })
            return results
            
        except Exception as e:
            print(f"Error fetching submissions: {e}")
            return []

# Global instance
github_service = GitHubService()
