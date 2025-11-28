#!/usr/bin/env python3
"""
Populates the workspace with content from the AIP-Notebook repository.
"""
import os
import sys
import shutil
import tempfile
import git

def populate_workspace():
    """Clone AIP-Notebook and copy content to workspace."""
    
    # Get workspace directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    workspace_dir = os.path.join(os.path.dirname(backend_dir), "workspace")
    
    print(f"Workspace directory: {workspace_dir}")
    
    # Create temp directory for cloning
    temp_dir = tempfile.mkdtemp(prefix="aip_notebook_clone_")
    print(f"Cloning to temporary directory: {temp_dir}")
    
    try:
        # Clone the AIP-Notebook repository
        repo_url = "https://github.com/Vexalabs/AIP-Notebook.git"
        print(f"Cloning {repo_url}...")
        repo = git.Repo.clone_from(repo_url, temp_dir)
        print("Clone successful!")
        
        # Directories to copy
        dirs_to_copy = ["notebooks", "sample_models"]
        files_to_copy = ["Readme.md", "gemini.md"]
        
        # Copy directories
        for dir_name in dirs_to_copy:
            src = os.path.join(temp_dir, dir_name)
            dst = os.path.join(workspace_dir, dir_name)
            
            if os.path.exists(src):
                # Remove existing directory if it exists
                if os.path.exists(dst):
                    print(f"Removing existing {dir_name}...")
                    shutil.rmtree(dst)
                
                print(f"Copying {dir_name}...")
                shutil.copytree(src, dst)
                print(f"  ✓ {dir_name} copied")
            else:
                print(f"  ⚠ {dir_name} not found in repository")
        
        # Copy files
        for file_name in files_to_copy:
            src = os.path.join(temp_dir, file_name)
            dst = os.path.join(workspace_dir, file_name)
            
            if os.path.exists(src):
                print(f"Copying {file_name}...")
                shutil.copy2(src, dst)
                print(f"  ✓ {file_name} copied")
            else:
                print(f"  ⚠ {file_name} not found in repository")
        
        print("\n✅ Workspace populated successfully!")
        print(f"Content available at: {workspace_dir}")
        
        # List what's in the workspace now
        print("\nWorkspace contents:")
        for item in os.listdir(workspace_dir):
            item_path = os.path.join(workspace_dir, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
        
    except Exception as e:
        print(f"❌ Error populating workspace: {e}")
        sys.exit(1)
    finally:
        # Clean up temp directory
        print(f"\nCleaning up temporary directory...")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print("Done!")

if __name__ == "__main__":
    populate_workspace()
