# ML Model Builder Environment

## 🎯 Project Overview

A self-contained, downloadable development environment that enables users to build, test, and submit custom ML models without complex setup. The system automates the entire workflow from model selection to deployment via GitHub pull requests.

---

## 🚀 The Problem We're Solving

Data scientists and ML engineers often face friction when deploying models:
- Complex infrastructure setup
- Environment configuration issues
- Deployment pipeline complexity
- Version control and collaboration challenges

**Our Solution:** A one-click downloadable executable that provides a complete, pre-configured development environment with automated deployment workflows.

---

## 📋 User Journey

### 1. **Download & Launch** (Entry Point)
- User clicks "Build Model" button in our web application
- Executable file (`.exe`) is downloaded
- User runs the executable locally

### 2. **Environment Initialization**
The executable spins up three integrated services:
- **React Frontend** - User interface for model selection and submission
- **FastAPI Backend** - Orchestration layer managing the workflow
- **Jupyter Notebook** - Interactive development environment with injected sample model

### 3. **Model Selection**
User interacts with the frontend to:
- Browse available notebook templates
- Select a sample model (starter code)
- Click "Start Building"

### 4. **Development Environment Setup**
Backend automatically:
- Pulls the latest code from the `main` branch of the designated repository
- Spins up a Jupyter Notebook instance
- Injects the selected sample model code
- Starts the model's FastAPI endpoint (each model runs as its own API)

**At this point, the user has:**
- ✅ Frontend tool (still running)
- ✅ Backend orchestration service (still running)
- ✅ Jupyter Notebook with sample model
- ✅ Model API endpoint (FastAPI) running locally

### 5. **Model Development**
User works in the Jupyter Notebook to:
- Experiment with the sample model
- Customize parameters and logic
- Test predictions via the local API
- Iterate until satisfied with results

### 6. **Model Submission**
When ready to deploy:
- User returns to the frontend tool
- Clicks "Submit Model"
- Backend automatically:
  - Commits the user's code changes
  - Pushes to a new feature branch
  - Creates a Pull Request to the main repository
  - Triggers CI/CD pipeline (if configured)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User's Local Machine                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   React FE   │◄────►│ FastAPI      │◄────►│  Jupyter  │ │
│  │   (Port      │      │ Backend      │      │  Notebook │ │
│  │   3000)      │      │ (Port 8000)  │      │           │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                      │                     │       │
│         │                      │                     │       │
│         └──────────────────────┼─────────────────────┘       │
│                                │                             │
│                                ▼                             │
│                     ┌──────────────────┐                     │
│                     │   Model API      │                     │
│                     │   (FastAPI)      │                     │
│                     │   (Port 8001)    │                     │
│                     └──────────────────┘                     │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  GitHub Repo    │
                   │  (Pull Request) │
                   └─────────────────┘
```

---

## 🔧 Technology Stack

### Frontend
- **React** - User interface
- **Axios** - API communication
- **TailwindCSS** - Styling (or your preferred CSS framework)

### Backend
- **FastAPI** - Orchestration API
- **Python 3.9+** - Core language
- **Jupyter** - Notebook server
- **GitPython** - Git operations
- **PyGithub** - GitHub API integration

### Infrastructure
- **Docker** (optional) - Containerization
- **GCP** - Cloud deployment (production)
- **GitHub Actions** - CI/CD pipeline

---

## 📁 Project Structure

```
model_builder_env/
├── .secrets/                    # ⚠️ GITIGNORED - Store sensitive data here
│   ├── config.json             # Your actual secrets (copy from template)
│   └── gcp-service-account.json
├── config.template.json         # Template for secrets configuration
├── frontend/                    # React application
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/                     # FastAPI orchestration service
│   ├── main.py
│   ├── services/
│   ├── models/
│   └── requirements.txt
├── notebooks/                   # Jupyter notebook templates
│   └── sample_models/
├── models/                      # User model code (generated)
├── infra/                       # Infrastructure & deployment
│   ├── docker/
│   └── scripts/
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT_PLAN.md
│   └── API.md
├── .gitignore
└── readme.md                    # This file
```

---

## 🔐 Security & Secrets Management

### Setup Your Secrets

1. **Copy the template:**
   ```bash
   cp config.template.json .secrets/config.json
   ```

2. **Fill in your actual values in `.secrets/config.json`:**
   - GCP Project ID
   - API Keys (OpenAI, Google, etc.)
   - Database credentials
   - GitHub token
   - Service account keys

3. **Never commit `.secrets/` directory** (already in .gitignore)

### What to Store in `.secrets/config.json`:
- ✅ GCP Project IDs and credentials
- ✅ API keys for external services
- ✅ Database connection strings
- ✅ GitHub personal access tokens
- ✅ JWT secrets and encryption keys

---

## 🚦 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- GCP account (for production deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd model_builder_env
   ```

2. **Set up secrets**
   ```bash
   cp config.template.json .secrets/config.json
   # Edit .secrets/config.json with your actual credentials
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

5. **Run the application**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --reload

   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

---

## 📚 Next Steps

See the following documents for detailed information:
- **[DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md)** - Detailed implementation roadmap
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Technical architecture deep-dive
- **[API.md](docs/API.md)** - API documentation

---

## 🤝 Contributing

This is an internal project. Please follow the development plan and coordinate with the team.

---

## 📝 License

Proprietary - All rights reserved