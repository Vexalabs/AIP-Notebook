# Secrets Management Guide

**Purpose:** Secure handling of sensitive information for the ML Model Builder Environment

**Last Updated:** 2025-11-25

---

## 🔐 Overview

This project requires various secrets and credentials to function:
- **GitHub Personal Access Token** - For creating pull requests
- **GCP Service Account** - For cloud deployments (optional)
- **API Keys** - For external services (optional)
- **Database Credentials** - If using persistent storage (optional)

**CRITICAL:** Never commit secrets to version control!

---

## 📁 Directory Structure

```
model_builder_env/
├── .secrets/                      # ⚠️ GITIGNORED - Your actual secrets
│   ├── config.json               # Main configuration file
│   ├── gcp-service-account.json  # GCP credentials
│   └── .env                      # Environment variables (alternative)
├── config.template.json          # Template to copy
└── .gitignore                    # Ensures .secrets/ is never committed
```

---

## 🚀 Quick Setup

### Step 1: Copy the Template

```bash
# Create .secrets directory
mkdir -p .secrets

# Copy template
cp config.template.json .secrets/config.json
```

### Step 2: Fill in Your Secrets

Edit `.secrets/config.json` with your actual values:

```json
{
  "gcp": {
    "project_id": "my-actual-project-id",
    "service_account_key_path": ".secrets/gcp-service-account.json",
    "bucket_name": "my-ml-models-bucket",
    "region": "us-central1"
  },
  "api_keys": {
    "openai_api_key": "sk-...",
    "anthropic_api_key": "sk-ant-...",
    "google_api_key": "AIza..."
  },
  "github": {
    "token": "ghp_YOUR_ACTUAL_TOKEN_HERE",
    "repo_owner": "your-github-username",
    "repo_name": "your-repo-name"
  },
  "database": {
    "connection_string": "postgresql://user:password@localhost:5432/dbname",
    "redis_url": "redis://localhost:6379"
  },
  "secrets": {
    "jwt_secret": "your-random-jwt-secret-here",
    "encryption_key": "your-32-byte-encryption-key"
  }
}
```

### Step 3: Verify Permissions

```bash
# Ensure only you can read the secrets
chmod 600 .secrets/config.json
```

---

## 🔑 Obtaining Required Secrets

### 1. GitHub Personal Access Token

**Why needed:** To create pull requests automatically

**How to get it:**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name: "ML Model Builder"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. Paste into `.secrets/config.json` under `github.token`

**Token format:** `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Security tips:**
- Use fine-grained tokens if possible (more secure)
- Set expiration date (e.g., 90 days)
- Rotate regularly
- Never share or commit

---

### 2. GCP Service Account (Optional)

**Why needed:** For cloud deployments and GCS storage

**How to get it:**

1. Go to [GCP Console](https://console.cloud.google.com)
2. Select your project (or create one)
3. Navigate to: IAM & Admin → Service Accounts
4. Click "Create Service Account"
5. Fill in details:
   - Name: `ml-model-builder`
   - Description: `Service account for ML model builder`
6. Grant roles:
   - `Storage Admin` (for GCS)
   - `Cloud Run Admin` (if using Cloud Run)
   - `Artifact Registry Writer` (for Docker images)
7. Click "Create Key" → JSON
8. Download the JSON file
9. Save it as `.secrets/gcp-service-account.json`
10. Update `.secrets/config.json`:
   ```json
   {
     "gcp": {
       "project_id": "your-gcp-project-id",
       "service_account_key_path": ".secrets/gcp-service-account.json"
     }
   }
   ```

---

### 3. API Keys (Optional)

**OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign in → API Keys
3. Create new secret key
4. Copy and save in `.secrets/config.json`

**Google AI API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Copy and save in `.secrets/config.json`

---

## 🛡️ Security Best Practices

### 1. Never Commit Secrets

**Already protected by `.gitignore`:**
```gitignore
.secrets/
*.env
*.key
*.pem
secrets.json
```

**Verify before committing:**
```bash
# Check what will be committed
git status

# If you accidentally staged secrets
git reset .secrets/
```

---

### 2. Use Environment Variables (Alternative)

Instead of `config.json`, you can use `.env` file:

**Create `.secrets/.env`:**
```bash
# GitHub
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO_OWNER=your-username
GITHUB_REPO_NAME=your-repo

# GCP
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_KEY_PATH=.secrets/gcp-service-account.json

# API Keys
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379

# Secrets
JWT_SECRET=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key
```

**Load in Python:**
```python
from dotenv import load_dotenv
import os

load_dotenv('.secrets/.env')

github_token = os.getenv('GITHUB_TOKEN')
```

---

### 3. Rotate Secrets Regularly

**Recommended rotation schedule:**
- GitHub tokens: Every 90 days
- API keys: Every 6 months
- Service account keys: Annually
- JWT secrets: After any security incident

**How to rotate:**
1. Generate new secret
2. Update `.secrets/config.json`
3. Test the application
4. Revoke old secret

---

### 4. Use Different Secrets for Different Environments

```
.secrets/
├── config.dev.json       # Development
├── config.staging.json   # Staging
└── config.prod.json      # Production
```

**Load based on environment:**
```python
import os
import json

env = os.getenv('ENVIRONMENT', 'dev')
config_path = f'.secrets/config.{env}.json'

with open(config_path) as f:
    config = json.load(f)
```

---

### 5. Encrypt Secrets at Rest (Advanced)

**Using `cryptography` library:**

```python
from cryptography.fernet import Fernet

# Generate key (do this once, save securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted = cipher.encrypt(b"my-secret-token")

# Decrypt
decrypted = cipher.decrypt(encrypted)
```

**Store encryption key separately** (e.g., environment variable, key management service)

---

## 🔍 Accessing Secrets in Code

### Backend (Python)

**Using JSON config:**
```python
# config.py
import json
from pathlib import Path
from typing import Dict, Any

class Config:
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        config_path = Path('.secrets/config.json')
        if not config_path.exists():
            raise FileNotFoundError(
                "Secrets file not found. "
                "Copy config.template.json to .secrets/config.json"
            )
        
        with open(config_path) as f:
            self._config = json.load(f)
    
    @property
    def github_token(self) -> str:
        return self._config['github']['token']
    
    @property
    def gcp_project_id(self) -> str:
        return self._config['gcp']['project_id']
    
    @property
    def openai_api_key(self) -> str:
        return self._config['api_keys']['openai_api_key']

# Usage
config = Config()
token = config.github_token
```

**Using environment variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv('.secrets/.env')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not set")
```

---

### Frontend (React)

**⚠️ NEVER expose secrets in frontend!**

**Instead, proxy through backend:**

```javascript
// ❌ WRONG - Never do this!
const API_KEY = 'sk-1234567890';

// ✅ CORRECT - Call backend endpoint
const response = await fetch('/api/protected-action', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ data: 'something' })
});
```

**Backend handles the secret:**
```python
@app.post("/api/protected-action")
async def protected_action(data: dict):
    # Backend uses the secret
    api_key = config.openai_api_key
    # Make API call with secret
    result = external_api.call(api_key, data)
    return result
```

---

## 🚨 What to Do If Secrets Are Exposed

### If you accidentally commit secrets:

1. **Immediately revoke the secret**
   - GitHub: Revoke token
   - GCP: Disable service account key
   - API providers: Regenerate key

2. **Remove from Git history**
   ```bash
   # Use BFG Repo-Cleaner or git filter-branch
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .secrets/config.json" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (⚠️ dangerous!)
   git push origin --force --all
   ```

3. **Generate new secrets**

4. **Update all environments**

5. **Notify team members**

---

## ✅ Verification Checklist

Before running the application:

- [ ] `.secrets/config.json` exists and is filled out
- [ ] GitHub token is valid and has correct permissions
- [ ] GCP service account key is valid (if using GCP)
- [ ] All required API keys are present
- [ ] File permissions are restrictive (`chmod 600`)
- [ ] `.secrets/` is in `.gitignore`
- [ ] No secrets in environment variables (unless using `.env`)
- [ ] Tested loading secrets in code

**Test command:**
```bash
# Run this to verify secrets load correctly
python -c "from backend.config import Config; c = Config(); print('✅ Secrets loaded successfully')"
```

---

## 📚 Additional Resources

- [GitHub Token Security](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GCP Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-service-accounts)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [12-Factor App Config](https://12factor.net/config)

---

## 🆘 Troubleshooting

### "Secrets file not found"
```bash
cp config.template.json .secrets/config.json
# Then edit .secrets/config.json
```

### "Invalid GitHub token"
- Check token hasn't expired
- Verify correct scopes (`repo`, `workflow`)
- Regenerate if necessary

### "GCP authentication failed"
- Verify service account key path is correct
- Check service account has required roles
- Ensure `GOOGLE_APPLICATION_CREDENTIALS` env var is set

### "Permission denied"
```bash
chmod 600 .secrets/config.json
```

---

**Document Owner:** Security Team  
**Last Updated:** 2025-11-25  
**Status:** ACTIVE
