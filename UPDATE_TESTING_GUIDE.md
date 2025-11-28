# Testing the Update Feature - Step by Step Guide

## 🎯 Objective
Test that the update mechanism correctly:
1. Detects new releases
2. Downloads and applies updates
3. Shows new sample models
4. Updates frontend theme/colors
5. Preserves user workspace

---

## 📋 Test Plan

### Phase 1: Initial Installation

1. **Create the First Release (v1.0.0)**
   ```powershell
   # In your current repo directory
   cd "\\wsl.localhost\Ubuntu\opt\docker\4C_Predictions\model_builder_env"
   
   # Create distribution package
   chmod +x create-package.sh && ./create-package.sh
   ```

2. **Push to GitHub and Create Release**
   ```powershell
   # Force push to main (if not already done)
   git push origin initial-release:main --force
   ```

3. **Create GitHub Release v1.0.0**
   - Go to: https://github.com/Vexalabs/AIP-Notebook/releases
   - Click "Create a new release"
   - Tag: `v1.0.0`
   - Title: "AIP Notebooks v1.0.0 - Initial Release"
   - Description: "First public release"
   - **Upload**: `dist/AIP-Model-Builder-Installer.tar.gz`
   - Click "Publish release"

4. **Install the Application**
   - Extract `AIP-Model-Builder-Installer.tar.gz` to a test location
   - Run `Install_Windows.bat` as Administrator
   - Launch `AIP-Notebook.bat` from Desktop
   - Verify it works and shows 2 sample models (Crypto, Soccer)

---

### Phase 2: Create Update (v1.1.0)

1. **Clone Repo to New Location**
   ```powershell
   # In a NEW directory (not your original)
   cd C:\Temp  # or any test location
   git clone https://github.com/Vexalabs/AIP-Notebook.git
   cd AIP-Notebook
   ```

2. **Add a New Sample Model**
   ```bash
   # Create new sample model directory
   mkdir -p sample_models/weather
   cd sample_models/weather
   
   # Create basic structure
   mkdir src tests
   touch src/__init__.py tests/__init__.py
   ```

   Create `sample_models/weather/src/main.py`:
   ```python
   from fastapi import FastAPI
   from pydantic import BaseModel
   
   app = FastAPI(title="Weather Prediction API")
   
   class WeatherRequest(BaseModel):
       city: str
       date: str
   
   class WeatherResponse(BaseModel):
       temperature: float
       condition: str
       confidence: float
   
   @app.get("/")
   def root():
       return {"model": "weather", "version": "1.0.0"}
   
   @app.post("/predict")
   def predict(request: WeatherRequest):
       return WeatherResponse(
           temperature=22.5,
           condition="Sunny",
           confidence=0.85
       )
   ```

   Create `sample_models/weather/README.md`:
   ```markdown
   # Weather Prediction Model
   
   Predicts weather conditions for a given city and date.
   
   ## API Endpoints
   - GET `/` - Model info
   - POST `/predict` - Get weather prediction
   ```

   Create `sample_models/weather/requirements.txt`:
   ```
   fastapi
   uvicorn
   pydantic
   ```

3. **Update Frontend Theme**
   
   Edit `frontend/src/App.jsx` - Change the color scheme:
   ```javascript
   // Find the color classes and change them
   // Example: Change from blue to purple theme
   // bg-blue-500 → bg-purple-500
   // text-blue-600 → text-purple-600
   ```

   Or create a simple visual change in `frontend/src/index.css`:
   ```css
   /* Add at the top */
   :root {
     --primary-color: #9333ea; /* Purple instead of blue */
   }
   ```

4. **Update VERSION File**
   ```powershell
   # Change VERSION from 1.0.0 to 1.1.0
   echo "1.1.0" > VERSION
   ```

5. **Commit and Push Changes**
   ```powershell
   git add .
   git commit -m "v1.1.0: Add Weather model and update theme
   
   - Added new Weather prediction sample model
   - Updated frontend theme to purple
   - Bumped version to 1.1.0"
   
   git push origin main
   ```

6. **Create Package for v1.1.0**
   ```bash
   # In WSL
   chmod +x create-package.sh && ./create-package.sh
   ```

7. **Create GitHub Release v1.1.0**
   - Go to: https://github.com/Vexalabs/AIP-Notebook/releases
   - Click "Create a new release"
   - Tag: `v1.1.0`
   - Title: "AIP Notebooks v1.1.0 - Weather Model & Theme Update"
   - Description:
     ```markdown
     ## What's New
     - 🌤️ New Weather prediction sample model
     - 🎨 Updated frontend theme (purple accent)
     - 🐛 Bug fixes and improvements
     ```
   - **Upload**: `dist/AIP-Model-Builder-Installer.tar.gz`
   - Click "Publish release"

---

### Phase 3: Test the Update

1. **Open Your Original Installation**
   - Launch the app using `AIP-Notebook.bat`
   - Open browser to http://localhost:3000

2. **Check for Updates**
   - Look for the "Update Available" banner at the top
   - It should show: "Version 1.1.0 is available"
   - Click "Update Now"

3. **Verify Update Process**
   - Watch the update progress
   - Should show: "Downloading update..."
   - Then: "Installing update..."
   - Finally: "Update complete! Please restart."

4. **Restart and Verify**
   - Close the application
   - Relaunch `AIP-Notebook.bat`
   - Open browser to http://localhost:3000

5. **Check What Updated**
   - ✅ Should see 3 sample models now (Crypto, Soccer, **Weather**)
   - ✅ Frontend theme should be purple (or whatever you changed)
   - ✅ Version should show 1.1.0
   - ✅ Your workspace files should still be there (preserved)

---

## 🔍 Troubleshooting

### Update Not Detected
- Check `VERSION` file in installation directory
- Verify GitHub release has the correct tag (v1.1.0)
- Check that `AIP-Model-Builder-Installer.tar.gz` is attached to release

### Update Fails
- Check browser console for errors
- Check backend logs: Look at terminal where backend is running
- Verify the release asset name is exactly: `AIP-Model-Builder-Installer.tar.gz`

### New Model Not Showing
- Verify the model was included in the package
- Check `sample_models/` directory after update
- Restart the application completely

### Theme Not Updated
- Hard refresh browser: Ctrl+Shift+R
- Clear browser cache
- Check if frontend was rebuilt: `cd frontend && npm run build`

---

## 📝 Expected Results

| Test | Expected Result | Pass/Fail |
|------|----------------|-----------|
| Update detected | Banner shows "v1.1.0 available" | ☐ |
| Download works | Progress shown, no errors | ☐ |
| Files updated | New files in installation dir | ☐ |
| Weather model appears | 3 models in UI | ☐ |
| Theme changed | Purple colors visible | ☐ |
| Version updated | Shows 1.1.0 in app | ☐ |
| Workspace preserved | User files still there | ☐ |

---

## 🚀 Quick Test Commands

```powershell
# 1. Check current version
cat "\\wsl.localhost\Ubuntu\home\YOUR_USER\MLModelBuilder\VERSION"

# 2. Check sample models
ls "\\wsl.localhost\Ubuntu\home\YOUR_USER\MLModelBuilder\sample_models"

# 3. Check if update downloaded
ls "\\wsl.localhost\Ubuntu\home\YOUR_USER\MLModelBuilder\.updates"

# 4. Force check for updates (in browser console)
fetch('http://localhost:8000/api/updates/check').then(r => r.json()).then(console.log)
```

---

## 💡 Tips

1. **Keep Original Installation**: Don't delete it until testing is complete
2. **Use Different Directories**: Clone to a new location for v1.1.0 changes
3. **Check GitHub First**: Ensure release is published before testing
4. **Watch Logs**: Keep terminal windows open to see any errors
5. **Test Incrementally**: Test each feature separately

---

## 🎯 Success Criteria

The update feature works correctly if:
- ✅ Update is automatically detected
- ✅ Download and installation complete without errors
- ✅ New sample model appears in the UI
- ✅ Frontend changes are visible
- ✅ User workspace is preserved
- ✅ Application restarts successfully with new version

---

**Ready to test!** Follow the phases in order and check off each step as you complete it.
