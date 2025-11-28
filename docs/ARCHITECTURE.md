# ML Model Builder Environment - Technical Architecture

**Version:** 1.0  
**Last Updated:** 2025-11-25  
**Status:** Design Phase

---

## 🎯 Architecture Goals

1. **Simplicity** - Easy to understand and maintain
2. **Isolation** - Each user session is independent
3. **Scalability** - Can handle multiple concurrent users
4. **Security** - Sandboxed execution, secure secrets management
5. **Reliability** - Graceful error handling and recovery

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER'S WEB BROWSER                           │
│                    (Main Application - Separate)                     │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ Downloads Executable
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DOWNLOADABLE EXECUTABLE                           │
│                  (Self-Contained Environment)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                   ORCHESTRATION LAYER                       │    │
│  │              (Process Manager / Docker Compose)             │    │
│  └────────────────────────────────────────────────────────────┘    │
│                           │                                          │
│         ┌─────────────────┼─────────────────┐                       │
│         │                 │                 │                       │
│         ▼                 ▼                 ▼                       │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐             │
│  │   React     │   │   FastAPI   │   │   Jupyter   │             │
│  │   Frontend  │   │   Backend   │   │   Server    │             │
│  │             │   │             │   │             │             │
│  │  Port 3000  │◄─►│  Port 8000  │◄─►│  Port 8888  │             │
│  └─────────────┘   └─────────────┘   └─────────────┘             │
│                           │                   │                     │
│                           │                   │                     │
│                           ▼                   ▼                     │
│                    ┌─────────────┐     ┌─────────────┐            │
│                    │  Git Ops    │     │   Notebook  │            │
│                    │  Service    │     │   Files     │            │
│                    └─────────────┘     └─────────────┘            │
│                           │                                         │
│                           ▼                                         │
│                    ┌─────────────┐                                 │
│                    │  Model API  │                                 │
│                    │  (FastAPI)  │                                 │
│                    │  Port 8001  │                                 │
│                    └─────────────┘                                 │
│                                                                      │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               │ GitHub API
                               ▼
                      ┌──────────────────┐
                      │   GitHub Repo    │
                      │  (Pull Requests) │
                      └──────────────────┘
```

---

## 📦 Component Details

### 1. Frontend (React Application)

**Purpose:** User interface for model selection, development tracking, and submission

**Technology Stack:**
- React 18+
- React Router (navigation)
- Axios (HTTP client)
- TailwindCSS (styling)
- React Query (data fetching)

**Key Features:**
- Template browser
- Sample model selector
- Real-time status dashboard
- Submission workflow
- Error notifications

**API Endpoints Used:**
```
GET  /api/templates          - List available templates
GET  /api/sample-models      - List sample models
POST /api/start-environment  - Start development environment
GET  /api/status             - Get current status
POST /api/submit-model       - Submit model for PR creation
GET  /api/logs               - Stream logs
```

**State Management:**
```javascript
{
  selectedTemplate: null,
  selectedModel: null,
  environmentStatus: 'idle' | 'starting' | 'running' | 'error',
  jupyterUrl: null,
  modelApiUrl: null,
  logs: [],
  error: null
}
```

---

### 2. Backend (FastAPI Orchestration Service)

**Purpose:** Coordinate all services, manage Git operations, handle submissions

**Technology Stack:**
- FastAPI
- Pydantic (validation)
- GitPython (Git operations)
- PyGithub (GitHub API)
- jupyter-client (Jupyter management)
- psutil (process management)

**Directory Structure:**
```
backend/
├── main.py                    # FastAPI app entry point
├── config.py                  # Configuration management
├── models/
│   ├── request_models.py      # Pydantic request models
│   └── response_models.py     # Pydantic response models
├── services/
│   ├── git_service.py         # Git operations
│   ├── github_service.py      # GitHub API integration
│   ├── jupyter_service.py     # Jupyter server management
│   ├── model_api_service.py   # User model API management
│   └── process_manager.py     # Process orchestration
├── routes/
│   ├── templates.py           # Template endpoints
│   ├── environment.py         # Environment management
│   └── submission.py          # Model submission
├── utils/
│   ├── logger.py              # Logging configuration
│   ├── port_manager.py        # Port allocation
│   └── validators.py          # Code validation
└── requirements.txt
```

**Core Services:**

#### 2.1 Git Service (`services/git_service.py`)
```python
class GitService:
    def clone_repository(self, repo_url: str, target_dir: str)
    def create_branch(self, branch_name: str)
    def commit_changes(self, message: str, files: List[str])
    def push_branch(self, branch_name: str)
    def get_diff(self) -> str
```

#### 2.2 GitHub Service (`services/github_service.py`)
```python
class GitHubService:
    def create_pull_request(
        self, 
        title: str, 
        body: str, 
        head_branch: str, 
        base_branch: str
    ) -> PullRequest
    def get_repository_info(self) -> Repository
    def validate_token(self) -> bool
```

#### 2.3 Jupyter Service (`services/jupyter_service.py`)
```python
class JupyterService:
    def start_server(self, notebook_dir: str) -> str  # Returns URL
    def stop_server(self)
    def inject_sample_model(self, notebook_path: str, model_code: str)
    def get_server_status(self) -> dict
    def create_notebook_from_template(self, template_name: str) -> str
```

#### 2.4 Model API Service (`services/model_api_service.py`)
```python
class ModelAPIService:
    def start_model_api(self, model_dir: str, port: int)
    def stop_model_api(self)
    def health_check(self) -> bool
    def get_api_url(self) -> str
```

#### 2.5 Process Manager (`services/process_manager.py`)
```python
class ProcessManager:
    def start_all_services(self, config: dict)
    def stop_all_services(self)
    def get_service_status(self, service_name: str) -> dict
    def restart_service(self, service_name: str)
    def cleanup(self)
```

---

### 3. Jupyter Notebook Environment

**Purpose:** Interactive development environment for model building

**Components:**
- Jupyter Server
- IPython kernel
- Notebook templates
- Sample model code

**Notebook Structure:**
```
notebooks/
├── templates/
│   ├── regression_template.ipynb
│   ├── classification_template.ipynb
│   ├── timeseries_template.ipynb
│   └── custom_template.ipynb
└── sample_models/
    ├── linear_regression/
    │   ├── model.py
    │   ├── api.py
    │   └── requirements.txt
    ├── random_forest/
    │   ├── model.py
    │   ├── api.py
    │   └── requirements.txt
    └── lstm_forecaster/
        ├── model.py
        ├── api.py
        └── requirements.txt
```

**Sample Model API Template:**
```python
# api.py - Template for user's model API
from fastapi import FastAPI
from pydantic import BaseModel
from model import predict

app = FastAPI()

class PredictionRequest(BaseModel):
    features: list

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
async def make_prediction(request: PredictionRequest):
    result = predict(request.features)
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

### 4. Model API (User's FastAPI Service)

**Purpose:** Serve predictions from user's trained model

**Lifecycle:**
1. User develops model in Jupyter
2. Backend extracts model code
3. Backend starts FastAPI server with user's code
4. User can test predictions locally
5. On submission, code is committed to Git

**Port Management:**
- Frontend: 3000
- Backend: 8000
- Jupyter: 8888
- Model API: 8001 (dynamically allocated if conflict)

---

## 🔐 Security Architecture

### 1. Secrets Management

**Storage Location:** `.secrets/config.json` (gitignored)

**Access Pattern:**
```python
# config.py
import json
from pathlib import Path

class Config:
    def __init__(self):
        secrets_path = Path(".secrets/config.json")
        if not secrets_path.exists():
            raise FileNotFoundError("Secrets file not found")
        
        with open(secrets_path) as f:
            self.secrets = json.load(f)
    
    @property
    def github_token(self) -> str:
        return self.secrets["github"]["token"]
    
    @property
    def gcp_project_id(self) -> str:
        return self.secrets["gcp"]["project_id"]
```

**Environment Variables (Alternative):**
```bash
# .env file (also gitignored)
GITHUB_TOKEN=ghp_xxxxx
GCP_PROJECT_ID=my-project
GCP_SERVICE_ACCOUNT_KEY_PATH=.secrets/gcp-sa.json
```

### 2. Code Sandboxing

**Approach:** Run user code in isolated environment

**Options:**
1. **Docker Container** (Recommended)
   - Each user session in separate container
   - Resource limits (CPU, memory)
   - Network isolation

2. **Python Virtual Environment**
   - Lightweight
   - Limited isolation
   - Good for development

**Implementation:**
```python
# Docker-based sandboxing
import docker

class Sandbox:
    def __init__(self):
        self.client = docker.from_env()
    
    def run_user_code(self, code_dir: str):
        container = self.client.containers.run(
            "python:3.9-slim",
            volumes={code_dir: {'bind': '/workspace', 'mode': 'rw'}},
            working_dir='/workspace',
            command='python api.py',
            detach=True,
            mem_limit='512m',
            cpu_quota=50000,  # 50% of one CPU
            network_mode='bridge'
        )
        return container
```

### 3. Code Validation

**Pre-Submission Checks:**
- Syntax validation
- Import scanning (detect malicious imports)
- File size limits
- Dependency scanning

```python
# validators.py
import ast

class CodeValidator:
    FORBIDDEN_IMPORTS = ['os', 'subprocess', 'sys']
    
    def validate_python_code(self, code: str) -> tuple[bool, str]:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        
        # Check for forbidden imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.FORBIDDEN_IMPORTS:
                        return False, f"Forbidden import: {alias.name}"
        
        return True, "Valid"
```

---

## 🔄 Data Flow

### Workflow: Start Development Environment

```
User (Frontend)
    │
    │ POST /api/start-environment
    │ { template: "regression", model: "linear_regression" }
    ▼
Backend (FastAPI)
    │
    ├─► Git Service
    │   └─► Clone repository to temp directory
    │
    ├─► Jupyter Service
    │   ├─► Create notebook from template
    │   ├─► Inject sample model code
    │   └─► Start Jupyter server
    │
    ├─► Model API Service
    │   ├─► Copy model code to workspace
    │   └─► Start FastAPI server
    │
    └─► Return URLs
        {
          jupyter_url: "http://localhost:8888",
          model_api_url: "http://localhost:8001",
          status: "running"
        }
```

### Workflow: Submit Model

```
User (Frontend)
    │
    │ POST /api/submit-model
    │ { commit_message: "My awesome model" }
    ▼
Backend (FastAPI)
    │
    ├─► Code Validator
    │   └─► Validate user's code
    │
    ├─► Git Service
    │   ├─► Create new branch (feature/model-{timestamp})
    │   ├─► Copy notebook and model files
    │   ├─► Commit changes
    │   └─► Push to remote
    │
    ├─► GitHub Service
    │   └─► Create Pull Request
    │       ├─► Title: "New model submission"
    │       ├─► Body: Auto-generated description
    │       └─► Labels: ["model-submission", "automated"]
    │
    └─► Cleanup
        ├─► Stop Jupyter server
        ├─► Stop Model API
        └─► Remove temp files
```

---

## 📊 Database Schema (Optional)

**Note:** For MVP, we may not need a database. All state is ephemeral.

**If needed for tracking submissions:**

```sql
-- submissions table
CREATE TABLE submissions (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    template_name VARCHAR(100),
    model_name VARCHAR(100),
    branch_name VARCHAR(255),
    pr_url VARCHAR(500),
    status VARCHAR(50), -- 'pending', 'merged', 'rejected'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- sessions table (track active development sessions)
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    jupyter_port INT,
    model_api_port INT,
    status VARCHAR(50), -- 'active', 'stopped'
    started_at TIMESTAMP,
    last_activity TIMESTAMP
);
```

---

## 🚀 Deployment Architecture

### Development Environment
```
Developer Machine
├── Frontend (npm run dev)
├── Backend (uvicorn --reload)
└── Jupyter (manual start)
```

### Packaged Executable
```
Single Executable File
├── Embedded Python Runtime
├── Embedded Node.js Runtime
├── All Dependencies
├── Frontend Build (static files)
├── Backend Code
└── Jupyter Distribution
```

**Packaging Tool Options:**
1. **PyInstaller + Electron**
   - PyInstaller for backend
   - Electron for frontend + orchestration
   - Size: ~300-500MB

2. **Docker Desktop Integration**
   - Distribute as Docker Compose file
   - Requires Docker Desktop installed
   - Size: ~100MB (download images on first run)

3. **Standalone Binary (Go + Python)**
   - Go binary as orchestrator
   - Embedded Python for backend
   - Size: ~200-300MB

---

## 🔍 Monitoring & Logging

### Logging Strategy

**Log Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

**Log Aggregation:**
```python
# logger.py
import logging
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    fh = logging.FileHandler(log_dir / f"{name}.log")
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
```

### Metrics to Track

**System Metrics:**
- CPU usage
- Memory usage
- Disk usage
- Network I/O

**Application Metrics:**
- Environment start time
- Submission success rate
- Error rates
- Active sessions

**User Metrics:**
- Time to first submission
- Number of submissions per user
- Template popularity
- Model type distribution

---

## 🧪 Testing Strategy

### Unit Tests
- Individual service functions
- Validators
- Utilities

### Integration Tests
- Full workflow tests
- API endpoint tests
- Git operations

### End-to-End Tests
- User journey simulation
- Frontend + Backend integration
- PR creation verification

**Test Structure:**
```
tests/
├── unit/
│   ├── test_git_service.py
│   ├── test_jupyter_service.py
│   └── test_validators.py
├── integration/
│   ├── test_environment_workflow.py
│   └── test_submission_workflow.py
└── e2e/
    └── test_full_user_journey.py
```

---

## 📈 Performance Considerations

### Optimization Targets
- Environment startup: < 30 seconds
- Jupyter launch: < 10 seconds
- Model API start: < 5 seconds
- PR creation: < 10 seconds

### Caching Strategy
- Cache cloned repositories
- Reuse Jupyter kernels
- Cache dependencies

### Resource Limits
- Max concurrent sessions: 5 (per user)
- Max model size: 100MB
- Max notebook size: 10MB
- Timeout for operations: 5 minutes

---

## 🔮 Future Enhancements

1. **Cloud Execution Mode**
   - Run environment in cloud (GCP Cloud Run)
   - Access via browser (no download needed)

2. **Collaboration Features**
   - Multiple users on same model
   - Real-time code sharing

3. **Model Versioning**
   - Track model iterations
   - A/B testing support

4. **Advanced Analytics**
   - Model performance tracking
   - Usage analytics dashboard

5. **Marketplace**
   - Share templates
   - Community models

---

**Document Owner:** Architecture Team  
**Review Date:** 2025-12-01  
**Status:** DRAFT
