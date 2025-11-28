# 📘 ML Model Builder - User Manual

Welcome to ML Model Builder! This guide will help you get started building and submitting machine learning models.

## 🚀 Getting Started

### After Installation

Once installation is complete, you'll find a **"ML Model Builder"** shortcut on your desktop.

**Double-click it to start the application!**

Your browser will automatically open to http://localhost:3000

### First-Time Setup

If this is your first time, you'll see a **setup wizard** that helps you configure GitHub integration.

#### Step 1: Welcome
Click "Get Started" to begin the setup process.

#### Step 2: Create GitHub Token
You'll need a GitHub Personal Access Token to submit your models.

**Don't worry!** The wizard provides a direct link and step-by-step instructions:

1. Click the link to open GitHub's token creation page
2. Set a name: "ML Model Builder Access"
3. Set expiration: 90 days (or your preference)
4. Select scope: **`repo`** or **`public_repo`**
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

#### Step 3: Enter Token
Paste your GitHub token into the wizard.

The app will:
- Validate the token with GitHub
- Check it has the right permissions
- Save it securely on your computer

#### Step 4: Success!
You're ready to build models! Click "Start Building Models!"

## 🛠️ Using ML Model Builder

### Starting Your Environment

1. **Click "Start Environment"** button
2. Wait a few seconds for Jupyter to launch
3. Status will change to **"RUNNING"** (green)
4. **Click "Open Jupyter Notebook"** to access your workspace

### Building Your Model

#### In Jupyter:
1. Navigate to `notebooks/Jupyter/`
2. Open `starter_notebook.ipynb` (or create a new one)
3. Write your model code
4. Test your model
5. Save your work

#### Need Inspiration?
- Check `sample_models/crypto/` for example code
- Review `README.md` for guidance
- Explore other notebooks in the `notebooks/` folder

### Submitting Your Model

When your model is ready:

1. **Return to ML Model Builder** (browser tab at http://localhost:3000)
2. **Fill in the submission form:**
   - **Commit Message:** Brief description (e.g., "Added LSTM model for crypto prediction")
   - **Description:** Detailed explanation of your changes
3. **Click "Submit to GitHub"**
4. Wait for confirmation
5. **Success!** You'll receive a link to your Pull Request

Your model is now submitted for review!

## 📁 Workspace Structure

Your workspace contains:

```
workspace/
├── notebooks/
│   ├── Jupyter/           # Jupyter notebooks
│   │   └── starter_notebook.ipynb
│   └── Marimo/            # Marimo notebooks
├── sample_models/
│   └── crypto/            # Example models
│       └── model.py
├── Readme.md              # Documentation
└── gemini.md              # Additional notes
```

## 🔓 Managing Your GitHub Token

### Updating Your Token

If you need to change your GitHub token:

1. Delete the configuration file:
   - Location: `%APPDATA%\MLModelBuilder\.secrets\config.json`
2. Restart the application
3. The setup wizard will appear again

### Token Security

Your token is stored locally on your computer in:
- `%APPDATA%\MLModelBuilder\.secrets\config.json`

**Never share your token with anyone!**

The token is only used to:
- Create Pull Requests on GitHub
- Validate your identity

## 🛑 Stopping the Application

To stop ML Model Builder:

**Option 1:** Press any key in the terminal window that opened when you started

**Option 2:** Double-click the **"Stop MLModelBuilder.bat"** shortcut (if you created one)

**Option 3:** Close the terminal window

## 🔧 Troubleshooting

### Application Won't Start

1. Make sure WSL is running:
   ```
   wsl --version
   ```
2. Check if services are already running:
   - Try accessing http://localhost:3000 directly
3. Restart your computer

### "Port Already in Use" Error

1. Stop any running instances
2. Open PowerShell as Administrator:
   ```powershell
   wsl -d Ubuntu bash -c "pkill -f uvicorn; pkill -f vite; pkill -f jupyter"
   ```
3. Try starting again

### GitHub Submission Fails

Check your token:
1. Make sure it has the right permissions (`repo` or `public_repo`)
2. Verify it hasn't expired
3. Re-run setup wizard to enter a new token

### Jupyter Won't Open

1. Make sure environment is **"RUNNING"** (green status)
2. Wait 5-10 seconds after starting
3. Click the "Open Jupyter Notebook" button again
4. Check for errors in the terminal window

## 💡 Tips & Best Practices

### Model Development
- **Save often** - Jupyter auto-saves, but don't rely on it completely
- **Test thoroughly** - Run all cells before submitting
- **Document your code** - Use markdown cells to explain your approach
- **Use meaningful names** - Name your files descriptively

### Submissions
- **Write clear commit messages** - Help reviewers understand your changes
- **Provide detailed descriptions** - Explain what your model does and why
- **Review before submitting** - Double-check your code
- **One feature per PR** - Don't mix multiple unrelated changes

### Performance
- **Clean up old notebooks** - Delete ones you don't need
- **Restart Jupyter periodically** - If it feels slow
- **Stop environment when done** - Frees up resources

## 📚 Additional Resources

### In Your Installation
- `QUICK_START_GUIDE.md` - Quick reference
- `WORKSPACE_STATUS.md` - What's in the workspace
- `README.md` - Project overview

### Online
- GitHub documentation: https://docs.github.com
- Jupyter tutorials: https://jupyter.org/try
- Python ML resources: https://scikit-learn.org

## 🆘 Getting Help

### Self-Help
1. Check this manual
2. Review error messages carefully
3. Search for similar issues online

### Community Support
- Check project README
- Submit an issue (if open source)
- Ask in community forums

### Contact Support
- Email: [your-support-email]
- Response time: 24-48 hours

---

## 🎉 Happy Model Building!

You're all set to create amazing machine learning models!

**Remember:**
1. Start the app from the desktop shortcut
2. Use the setup wizard (first time only)
3. Build models in Jupyter
4. Submit via the web interface

**Have fun, and good luck with your models!** 🚀
