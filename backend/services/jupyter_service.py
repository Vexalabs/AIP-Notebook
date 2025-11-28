import subprocess
import os
import sys
import time
import psutil
from pathlib import Path
from typing import Optional, Dict

class JupyterService:
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.port = 8888
        self.token = "modelbuilder"  # Fixed token for MVP simplicity
        
    def start_server(self, notebook_dir: str) -> Dict[str, str]:
        """
        Starts a Jupyter notebook server in the specified directory.
        """
        if self.is_running():
            return {
                "status": "running",
                "url": f"http://localhost:{self.port}/tree?token={self.token}",
                "message": "Server already running"
            }

        # Ensure directory exists
        os.makedirs(notebook_dir, exist_ok=True)

        # Use sys.executable to ensure we use the same python environment
        cmd = [
            sys.executable, "-m", "jupyter", "notebook",
            "--no-browser",
            f"--port={self.port}",
            f"--NotebookApp.token={self.token}",
            f"--notebook-dir={notebook_dir}",
            "--allow-root"  # Needed if running in docker
        ]

        print(f"Starting Jupyter with command: {' '.join(cmd)}")

        try:
            # Start process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit to check for immediate failures
            time.sleep(2)
            if self.process.poll() is not None:
                stdout, stderr = self.process.communicate()
                print(f"Jupyter failed to start. Stdout: {stdout}, Stderr: {stderr}")
                raise Exception(f"Jupyter exited immediately. Error: {stderr}")

            print(f"Jupyter started successfully on port {self.port}")
            return {
                "status": "started",
                "url": f"http://localhost:{self.port}/tree?token={self.token}",
                "token": self.token
            }
            
        except Exception as e:
            print(f"Error starting Jupyter: {e}")
            return {"status": "error", "message": str(e)}

    def stop_server(self):
        """Stops the Jupyter server."""
        if self.process:
            # Kill the process tree (jupyter spawns children)
            parent = psutil.Process(self.process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
            parent.wait()  # Wait for process to exit
            self.process = None
            return {"status": "stopped"}
        return {"status": "not_running"}

    def is_running(self) -> bool:
        """Checks if the server is running."""
        if self.process is None:
            return False
        return self.process.poll() is None

# Global instance
jupyter_service = JupyterService()
