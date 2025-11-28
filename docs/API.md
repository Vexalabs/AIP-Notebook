# API Documentation

**Service:** ML Model Builder Backend  
**Base URL:** `http://localhost:8000`  
**Version:** 1.0  
**Protocol:** REST API (JSON)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
   - [Health & Status](#health--status)
   - [Templates](#templates)
   - [Environment Management](#environment-management)
   - [Model Submission](#model-submission)
   - [Logs](#logs)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)

---

## 🔐 Authentication

**Current:** No authentication required (local development only)

**Future (Production):**
```http
Authorization: Bearer <token>
```

---

## 📡 Endpoints

### Health & Status

#### `GET /health`
Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-25T12:47:40Z"
}
```

---

#### `GET /api/status`
Get current environment status.

**Response:**
```json
{
  "environment_status": "running",
  "services": {
    "jupyter": {
      "status": "running",
      "url": "http://localhost:8888",
      "port": 8888
    },
    "model_api": {
      "status": "running",
      "url": "http://localhost:8001",
      "port": 8001
    }
  },
  "session_id": "uuid-here",
  "started_at": "2025-11-25T12:30:00Z",
  "uptime_seconds": 1060
}
```

---

### Templates

#### `GET /api/templates`
List all available notebook templates.

**Response:**
```json
{
  "templates": [
    {
      "id": "regression",
      "name": "Linear Regression",
      "description": "Template for regression problems",
      "difficulty": "beginner",
      "tags": ["supervised", "regression"],
      "preview_url": "/templates/regression/preview.png"
    },
    {
      "id": "classification",
      "name": "Classification",
      "description": "Template for classification problems",
      "difficulty": "intermediate",
      "tags": ["supervised", "classification"],
      "preview_url": "/templates/classification/preview.png"
    }
  ]
}
```

---

#### `GET /api/sample-models`
List all available sample models.

**Query Parameters:**
- `template_id` (optional): Filter by template

**Response:**
```json
{
  "models": [
    {
      "id": "linear_regression",
      "name": "Linear Regression",
      "template_id": "regression",
      "description": "Simple linear regression model",
      "language": "python",
      "framework": "scikit-learn",
      "file_count": 3,
      "size_kb": 12
    },
    {
      "id": "random_forest",
      "name": "Random Forest Classifier",
      "template_id": "classification",
      "description": "Ensemble tree-based classifier",
      "language": "python",
      "framework": "scikit-learn",
      "file_count": 4,
      "size_kb": 18
    }
  ]
}
```

---

### Environment Management

#### `POST /api/start-environment`
Start the development environment with selected template and model.

**Request Body:**
```json
{
  "template_id": "regression",
  "model_id": "linear_regression",
  "user_id": "user-123",
  "config": {
    "jupyter_port": 8888,
    "model_api_port": 8001
  }
}
```

**Response (Success):**
```json
{
  "status": "success",
  "session_id": "uuid-here",
  "jupyter_url": "http://localhost:8888",
  "jupyter_token": "token-here",
  "model_api_url": "http://localhost:8001",
  "workspace_path": "/tmp/workspace-uuid",
  "message": "Environment started successfully"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "error_code": "PORT_IN_USE",
  "message": "Port 8888 is already in use",
  "details": {
    "conflicting_port": 8888,
    "suggested_port": 8889
  }
}
```

---

#### `POST /api/stop-environment`
Stop the current development environment.

**Request Body:**
```json
{
  "session_id": "uuid-here",
  "cleanup": true
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Environment stopped and cleaned up",
  "stopped_services": ["jupyter", "model_api"],
  "cleaned_files": true
}
```

---

#### `POST /api/restart-service`
Restart a specific service.

**Request Body:**
```json
{
  "session_id": "uuid-here",
  "service": "model_api"
}
```

**Response:**
```json
{
  "status": "success",
  "service": "model_api",
  "new_url": "http://localhost:8001",
  "message": "Service restarted successfully"
}
```

---

### Model Submission

#### `POST /api/submit-model`
Submit the model for review (creates GitHub PR).

**Request Body:**
```json
{
  "session_id": "uuid-here",
  "commit_message": "Add improved linear regression model",
  "description": "This model improves accuracy by 15%",
  "metadata": {
    "model_type": "regression",
    "framework": "scikit-learn",
    "accuracy": 0.92
  }
}
```

**Response (Success):**
```json
{
  "status": "success",
  "pr_url": "https://github.com/org/repo/pull/123",
  "pr_number": 123,
  "branch_name": "feature/model-1732537660",
  "commit_sha": "abc123def456",
  "message": "Pull request created successfully"
}
```

**Response (Validation Error):**
```json
{
  "status": "error",
  "error_code": "VALIDATION_FAILED",
  "message": "Code validation failed",
  "validation_errors": [
    {
      "file": "model.py",
      "line": 42,
      "error": "Forbidden import: os"
    }
  ]
}
```

---

#### `GET /api/submission-status/{pr_number}`
Check the status of a submitted model.

**Response:**
```json
{
  "pr_number": 123,
  "status": "open",
  "checks": {
    "ci_passed": true,
    "code_review": "pending",
    "tests_passed": true
  },
  "reviewers": ["reviewer1", "reviewer2"],
  "comments_count": 3,
  "updated_at": "2025-11-25T13:00:00Z"
}
```

---

### Logs

#### `GET /api/logs`
Stream logs from the environment.

**Query Parameters:**
- `session_id`: Session identifier
- `service`: Service name (`jupyter`, `model_api`, `backend`)
- `level`: Log level (`debug`, `info`, `warning`, `error`)
- `tail`: Number of recent lines (default: 100)

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-11-25T12:45:00Z",
      "level": "INFO",
      "service": "jupyter",
      "message": "Jupyter server started on port 8888"
    },
    {
      "timestamp": "2025-11-25T12:45:05Z",
      "level": "INFO",
      "service": "model_api",
      "message": "Model API started on port 8001"
    }
  ],
  "total_lines": 2,
  "session_id": "uuid-here"
}
```

---

#### `GET /api/logs/stream` (WebSocket)
Real-time log streaming.

**WebSocket URL:** `ws://localhost:8000/api/logs/stream`

**Message Format:**
```json
{
  "timestamp": "2025-11-25T12:45:00Z",
  "level": "INFO",
  "service": "jupyter",
  "message": "Cell executed successfully"
}
```

---

## 📊 Data Models

### Template
```typescript
interface Template {
  id: string;
  name: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  tags: string[];
  preview_url: string;
}
```

### SampleModel
```typescript
interface SampleModel {
  id: string;
  name: string;
  template_id: string;
  description: string;
  language: string;
  framework: string;
  file_count: number;
  size_kb: number;
}
```

### EnvironmentConfig
```typescript
interface EnvironmentConfig {
  template_id: string;
  model_id: string;
  user_id: string;
  config?: {
    jupyter_port?: number;
    model_api_port?: number;
  };
}
```

### EnvironmentStatus
```typescript
interface EnvironmentStatus {
  environment_status: 'idle' | 'starting' | 'running' | 'stopping' | 'error';
  services: {
    jupyter: ServiceInfo;
    model_api: ServiceInfo;
  };
  session_id: string;
  started_at: string;
  uptime_seconds: number;
}

interface ServiceInfo {
  status: 'running' | 'stopped' | 'error';
  url: string;
  port: number;
}
```

### SubmissionRequest
```typescript
interface SubmissionRequest {
  session_id: string;
  commit_message: string;
  description?: string;
  metadata?: Record<string, any>;
}
```

### SubmissionResponse
```typescript
interface SubmissionResponse {
  status: 'success' | 'error';
  pr_url?: string;
  pr_number?: number;
  branch_name?: string;
  commit_sha?: string;
  message: string;
  validation_errors?: ValidationError[];
}

interface ValidationError {
  file: string;
  line: number;
  error: string;
}
```

---

## ❌ Error Handling

### Error Response Format
```json
{
  "status": "error",
  "error_code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {},
  "timestamp": "2025-11-25T12:47:40Z",
  "request_id": "uuid-here"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Invalid request parameters |
| `TEMPLATE_NOT_FOUND` | 404 | Template ID not found |
| `MODEL_NOT_FOUND` | 404 | Model ID not found |
| `SESSION_NOT_FOUND` | 404 | Session ID not found |
| `PORT_IN_USE` | 409 | Requested port is already in use |
| `ENVIRONMENT_ALREADY_RUNNING` | 409 | Environment already running |
| `VALIDATION_FAILED` | 422 | Code validation failed |
| `GIT_ERROR` | 500 | Git operation failed |
| `GITHUB_API_ERROR` | 502 | GitHub API error |
| `SERVICE_START_FAILED` | 500 | Failed to start service |
| `INTERNAL_ERROR` | 500 | Internal server error |

---

## 🚦 Rate Limiting

**Current:** No rate limiting (local development)

**Future (Production):**
- 100 requests per minute per user
- 10 environment starts per hour per user
- 5 submissions per day per user

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1732537800
```

---

## 🔄 Versioning

API versioning via URL path:
- Current: `http://localhost:8000/api/...`
- Future: `http://localhost:8000/v2/api/...`

---

## 📝 Examples

### Complete Workflow Example (JavaScript)

```javascript
const API_BASE = 'http://localhost:8000';

// 1. Check health
const health = await fetch(`${API_BASE}/health`);
console.log(await health.json());

// 2. Get templates
const templates = await fetch(`${API_BASE}/api/templates`);
const { templates: templateList } = await templates.json();

// 3. Get sample models
const models = await fetch(`${API_BASE}/api/sample-models`);
const { models: modelList } = await models.json();

// 4. Start environment
const startEnv = await fetch(`${API_BASE}/api/start-environment`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    template_id: 'regression',
    model_id: 'linear_regression',
    user_id: 'user-123'
  })
});
const { session_id, jupyter_url } = await startEnv.json();

// 5. Check status
const status = await fetch(`${API_BASE}/api/status`);
console.log(await status.json());

// 6. Submit model
const submit = await fetch(`${API_BASE}/api/submit-model`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id,
    commit_message: 'My awesome model',
    description: 'Improved accuracy'
  })
});
const { pr_url } = await submit.json();
console.log('PR created:', pr_url);
```

---

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Get templates
curl http://localhost:8000/api/templates

# Start environment
curl -X POST http://localhost:8000/api/start-environment \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "regression",
    "model_id": "linear_regression",
    "user_id": "test-user"
  }'

# Submit model
curl -X POST http://localhost:8000/api/submit-model \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "commit_message": "Test submission"
  }'
```

---

**Document Owner:** API Team  
**Last Updated:** 2025-11-25  
**Status:** DRAFT
