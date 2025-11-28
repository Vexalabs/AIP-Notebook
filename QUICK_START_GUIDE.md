# 🚀 ML Model Builder - Quick Start

## Starting the Application

### Option 1: Double-Click to Start (Easiest)
1. Navigate to the project folder in Windows Explorer
2. **Double-click `start.bat`**
3. The browser will automatically open to http://localhost:3000
4. When you're done, press any key in the terminal window to stop

### Option 2: Manual Start
If you prefer manual control:
```bash
# In WSL terminal
cd /opt/docker/4C_Predictions/model_builder_env
./run.sh
```

## Stopping the Application

### Option 1: Double-Click to Stop
- **Double-click `stop.bat`** to cleanly shut down all services

### Option 2: Press Key
- If you started with `start.bat`, just press any key in the terminal window

### Option 3: Manual Stop
```bash
# In WSL terminal
wsl -d Ubuntu bash -c "pkill -f uvicorn; pkill -f vite; pkill -f jupyter"
```

## 📍 Access Points

Once started, you can access:
- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Jupyter Notebook:** http://localhost:8888/tree?token=modelbuilder (after starting environment)

## 🎯 Using the Application

### Step 1: Start Environment
1. Open http://localhost:3000
2. Click **"Start Environment"**
3. Wait for Jupyter to launch (status will show "RUNNING")

### Step 2: Develop Your Model
1. Click **"Open Jupyter Notebook"**
2. Navigate to `notebooks/Jupyter/`
3. Open `starter_notebook.ipynb`
4. Write your model code

### Step 3: Submit to GitHub
1. Return to the frontend (http://localhost:3000)
2. Fill in:
   - **Commit Message:** Brief description of your changes
   - **Description:** Detailed explanation for the PR
3. Click **"Submit to GitHub"**
4. A Pull Request will be created automatically!

## 📁 Workspace Structure

```
workspace/
├── notebooks/
│   ├── Jupyter/
│   │   └── starter_notebook.ipynb
│   └── Marimo/
│       └── getting_started.py
├── sample_models/
│   └── crypto/
│       └── model.py
├── Readme.md
└── gemini.md
```

## 🔧 Configuration

### Secrets
Secrets are configured in `.secrets/config.json`:
- **GCP Project ID:** For Google Secret Manager
- **GitHub Token:** For creating Pull Requests
- **Repository:** Target repo for submissions

### Changing Configuration
Edit `.secrets/config.json` and restart the services.

## 🆘 Troubleshooting

### Services Won't Start
1. Stop all running instances: double-click `stop.bat`
2. Check that WSL is running: `wsl -d Ubuntu echo "WSL is running"`
3. Try starting again: double-click `start.bat`

### Port Already in Use
If you see "Port 3001 is in use":
1. Stop all services with `stop.bat`
2. Manual cleanup: `wsl -d Ubuntu bash -c "pkill -f node"`
3. Start again

### GitHub Submission Fails
1. Check your token has correct permissions (public_repo or repo scope)
2. Verify token in `.secrets/config.json`
3. Restart services to reload configuration

## 📞 Need Help?

Check the documentation:
- **WORKSPACE_STATUS.md** - Workspace content overview
- **docs/API.md** - API documentation
- **docs/ARCHITECTURE.md** - System architecture
- **docs/SECRETS_MANAGEMENT.md** - Secrets setup guide

---

**Ready to build models? Just double-click `start.bat` and you're good to go!** 🚀
