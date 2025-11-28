import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel
from google.cloud import secretmanager
import google.auth

class GCPConfig(BaseModel):
    project_id: str
    service_account_key_path: Optional[str] = None
    bucket_name: Optional[str] = None
    region: str = "us-central1"

class APIKeys(BaseModel):
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

class GitHubConfig(BaseModel):
    token: Optional[str] = None
    repo_owner: str
    repo_name: str
    token_secret_name: Optional[str] = None # Name in GSM

class DatabaseConfig(BaseModel):
    connection_string: Optional[str] = None
    redis_url: Optional[str] = None

class SecretsConfig(BaseModel):
    jwt_secret: Optional[str] = None
    encryption_key: Optional[str] = None

class AppConfig(BaseModel):
    gcp: Optional[GCPConfig] = None
    api_keys: Optional[APIKeys] = None
    github: Optional[GitHubConfig] = None
    database: Optional[DatabaseConfig] = None
    secrets: Optional[SecretsConfig] = None

class Config:
    _instance = None
    _config: Optional[AppConfig] = None
    _gsm_client = None
    
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    WORKSPACE_DIR: Path = PROJECT_ROOT / "workspace"
    SAMPLE_MODELS_DIR: Path = PROJECT_ROOT / "sample_models"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        print("Loading configuration...")
        # 1. Load local config.json
        config_path = self.PROJECT_ROOT / ".secrets" / "config.json"
        
        if config_path.exists():
            print(f"Found config file at {config_path}")
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    self._config = AppConfig(**data)
                    print(f"Loaded config data: {data.keys()}")
            except Exception as e:
                print(f"ERROR: Failed to load config file: {e}")
                self._config = AppConfig()
        else:
            print(f"WARNING: Local config file not found at {config_path}")
            self._config = AppConfig()

        # 2. Try to fetch secrets from GSM if configured
        if self._config.gcp and self._config.gcp.project_id:
            print(f"Attempting to fetch secrets from GSM for project {self._config.gcp.project_id}...")
            self._fetch_gsm_secrets()
        else:
            print("GCP Project ID not configured, skipping GSM.")

    def _fetch_gsm_secrets(self):
        """Fetches secrets from Google Secret Manager."""
        try:
            # Initialize client (uses default credentials or service account)
            if not self._gsm_client:
                print("Initializing GSM client...")
                self._gsm_client = secretmanager.SecretManagerServiceClient()
            
            project_id = self._config.gcp.project_id
            
            # Fetch GitHub Token
            if self._config.github:
                # If token is already set in config (e.g. from local file), use it
                if self._config.github.token:
                    print("Using GitHub token from local configuration.")
                    return

                if self._config.github.token_secret_name:
                    secret_name = self._config.github.token_secret_name
                    print(f"Fetching secret: {secret_name}")
                # Handle full resource name or short name
                if not secret_name.startswith("projects/"):
                    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
                else:
                    name = secret_name
                
                try:
                    print(f"Accessing secret version: {name}")
                    response = self._gsm_client.access_secret_version(request={"name": name})
                    token_str = response.payload.data.decode("UTF-8")
                    
                    # Try to parse as JSON
                    try:
                        token_json = json.loads(token_str)
                        if isinstance(token_json, dict):
                            # Look for common keys
                            for key in ['API_TOKEN', 'token', 'GITHUB_TOKEN', 'github_token', 'pat']:
                                if key in token_json:
                                    token = token_json[key]
                                    break
                            else:
                                # Fallback: use the first value or the whole string if no known key
                                print(f"WARNING: JSON secret found but no known key (API_TOKEN, token, etc). Using first value.")
                                token = list(token_json.values())[0]
                        else:
                            token = token_str
                    except json.JSONDecodeError:
                        # Not JSON, use raw string
                        token = token_str.strip()
                        
                    self._config.github.token = token
                    print(f"Successfully loaded GitHub token from GSM: {secret_name}")
                except Exception as e:
                    print(f"Failed to fetch GitHub token from GSM: {e}")

        except Exception as e:
            print(f"Failed to initialize GSM client: {e}")

    @property
    def github_token(self) -> Optional[str]:
        return self._config.github.token if self._config.github else None

    @property
    def github_repo(self) -> Optional[str]:
        if self._config.github:
            return f"{self._config.github.repo_owner}/{self._config.github.repo_name}"
        return None


    def reload(self):
        """Force reload of configuration from disk."""
        print("Reloading configuration...")
        self._load_config()
    
    def get(self) -> AppConfig:
        return self._config

# Global instance
config = Config()
