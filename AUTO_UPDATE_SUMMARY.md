# Auto-Update System - Quick Summary

## Current State ✅

**What's Working:**
- ✅ Update detection via GitHub API
- ✅ Frontend banner shows when update is available
- ✅ "Update Now" button triggers update process
- ✅ Version comparison logic

**What's Broken/Missing:**
- ❌ Uses archive download instead of `git pull`
- ❌ Only works on Linux/WSL (not Windows native or Mac)
- ❌ Version in UI is hardcoded, not dynamic
- ❌ Poor user feedback during update
- ❌ No rollback if update fails
- ❌ May lose user data if update fails

---

## What Needs to Be Done 🎯

### Critical (Must Fix)

1. **Switch to Git-Based Updates**
   - Change from downloading `.tar.gz` to using `git pull origin main`
   - Simpler, faster, more reliable
   - Leverages existing Git infrastructure

2. **Make It Cross-Platform**
   - Detect OS (Windows/WSL, Mac, Linux)
   - Generate appropriate update script for each platform
   - Test on all platforms

3. **Fix Version Display**
   - Currently shows hardcoded "v1.0.0"
   - Should fetch from backend API dynamically
   - Update on every app load

4. **Better User Feedback**
   - Show progress: "Downloading...", "Installing...", "Restarting..."
   - Poll backend for status updates
   - Clear success/failure messages

### Important (Should Have)

5. **Backup Before Update**
   - Create backup of workspace and .secrets
   - If update fails, can restore
   - Prevents data loss

6. **Validate Before Update**
   - Check: Is Git installed?
   - Check: Is this a Git repo?
   - Check: Is there internet connection?
   - Check: Enough disk space?
   - Show clear error if prerequisites not met

### Nice to Have

7. **Rollback Feature**
   - If update fails, one-click rollback
   - Restore from backup
   - Checkout previous Git commit

8. **Show Release Notes**
   - Display what's new in the update
   - Help users decide if they want to update now

---

## Implementation Approach

### Step 1: Update Backend (`backend/routes/updates.py`)

```python
@router.post("/perform")
async def perform_update():
    # 1. Check if Git repo
    # 2. Create backup
    # 3. Generate update script:
    #    - git pull origin main
    #    - pip install -r requirements.txt
    #    - npm install && npm run build
    #    - restart services
    # 4. Execute script in background
    # 5. Return success
```

### Step 2: Update Frontend (`frontend/src/App.jsx`)

```javascript
// Fetch version dynamically
const [currentVersion, setCurrentVersion] = useState('...')
useEffect(() => {
    axios.get('/api/updates/current-version')
        .then(res => setCurrentVersion(res.data.version))
}, [])

// Better update feedback
const performUpdate = async () => {
    setUpdateProgress("Starting update...")
    await axios.post('/api/updates/perform')
    
    // Poll for status
    const interval = setInterval(async () => {
        const status = await axios.get('/api/updates/status')
        setUpdateProgress(status.data.message)
        if (status.data.complete) {
            clearInterval(interval)
            window.location.reload()
        }
    }, 2000)
}
```

### Step 3: Create Platform-Specific Scripts

**Linux/WSL/Mac:**
```bash
#!/bin/bash
cd /path/to/app
git pull origin main
pip install -r backend/requirements.txt
cd frontend && npm install && npm run build
pkill -f uvicorn && pkill -f vite
nohup ./run.sh &
```

**Windows (PowerShell):**
```powershell
wsl -d Ubuntu bash -c "cd ~/MLModelBuilder && git pull origin main"
wsl -d Ubuntu bash -c "cd ~/MLModelBuilder && ./setup.sh"
wsl -d Ubuntu bash -c "cd ~/MLModelBuilder && ./run.sh"
```

---

## Testing Checklist

- [ ] Create v1.0.0 release on GitHub
- [ ] Install v1.0.0 locally
- [ ] Make visible changes (add new sample model, change theme color)
- [ ] Update VERSION to 1.1.0
- [ ] Push to GitHub and create v1.1.0 release
- [ ] Open v1.0.0 app
- [ ] Verify update banner appears
- [ ] Click "Update Now"
- [ ] Verify progress messages show
- [ ] Verify app restarts automatically
- [ ] Verify new features are present
- [ ] Verify workspace files are intact
- [ ] Test on Windows, Mac, and Linux

---

## Quick Wins (Do These First)

1. **Dynamic Version Display** (5 minutes)
   - Change `v1.0.0` to `v{currentVersion}` in App.jsx
   - Fetch from `/api/updates/current-version` on load

2. **Better Update Button Feedback** (10 minutes)
   - Show loading spinner when clicked
   - Disable button during update
   - Show "Update in progress..." message

3. **Git Pull Instead of Archive** (30 minutes)
   - Replace archive download logic with `git pull`
   - Test on WSL first

---

## Files to Modify

1. `backend/routes/updates.py` - Main update logic
2. `frontend/src/App.jsx` - UI and version display
3. `VERSION` - Keep updated with releases
4. `AUTO_UPDATE_SPECIFICATION.md` - Full detailed spec (already created)

---

## Success Metrics

✅ **Update works when:**
- User sees banner within 5 seconds of new release
- Update completes in under 2 minutes
- App restarts automatically
- User data is preserved
- Works on all platforms (Windows/WSL, Mac, Linux)

❌ **Update fails if:**
- User loses workspace data
- App doesn't restart
- Update takes longer than 5 minutes
- Errors are not clearly communicated

---

## Next Action

**Recommended:** Start with Phase 1 (Core Functionality) from the full specification:
1. Implement Git-based updates
2. Add dynamic version display
3. Improve progress feedback
4. Test on WSL

Then move to Phase 2 (Safety) and Phase 3 (UX enhancements).

See `AUTO_UPDATE_SPECIFICATION.md` for complete implementation details.
