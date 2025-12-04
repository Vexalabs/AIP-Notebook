# Auto-Update Implementation Checklist

## 📋 Phase 1: Core Functionality (Must Have)

### Backend Changes

- [ ] **Update `backend/routes/updates.py`**
  - [ ] Add platform detection (Windows/WSL, Mac, Linux)
  - [ ] Replace archive download with Git pull logic
  - [ ] Add `validate_update_prerequisites()` function
  - [ ] Add `create_backup()` function
  - [ ] Create platform-specific update script generators
  - [ ] Add `/api/updates/status` endpoint for progress tracking
  - [ ] Update `/api/updates/perform` to use Git pull
  - [ ] Add proper error handling and logging

- [ ] **Create Update Script Templates**
  - [ ] `backend/scripts/update-unix.sh.template`
  - [ ] `backend/scripts/update-windows.ps1.template`
  - [ ] Make scripts executable and test on each platform

### Frontend Changes

- [ ] **Update `frontend/src/App.jsx`**
  - [ ] Add `currentVersion` state variable
  - [ ] Add `fetchCurrentVersion()` function
  - [ ] Replace hardcoded "v1.0.0" with dynamic `{currentVersion}`
  - [ ] Add `updateProgress` state for status messages
  - [ ] Update `performUpdate()` to poll for status
  - [ ] Add progress indicator UI
  - [ ] Improve error messages

- [ ] **Enhance Update Banner**
  - [ ] Add loading spinner during update
  - [ ] Show real-time progress messages
  - [ ] Add release notes section (expandable)
  - [ ] Disable button during update

### Testing

- [ ] **Test on WSL/Linux**
  - [ ] Create test release v1.0.1
  - [ ] Verify update detection
  - [ ] Verify Git pull works
  - [ ] Verify dependencies update
  - [ ] Verify app restarts
  - [ ] Verify workspace preserved

- [ ] **Test on Mac**
  - [ ] Same tests as WSL/Linux

- [ ] **Test on Windows (if native support added)**
  - [ ] Same tests as above

---

## 📋 Phase 2: Safety & Reliability (Should Have)

### Backup System

- [ ] **Implement Pre-Update Backup**
  - [ ] Create `create_backup()` function
  - [ ] Backup workspace directory
  - [ ] Backup .secrets directory
  - [ ] Backup VERSION file
  - [ ] Store backup with timestamp
  - [ ] Add backup location to update response

### Validation System

- [ ] **Implement Pre-Update Validation**
  - [ ] Check Git is installed
  - [ ] Check current directory is Git repo
  - [ ] Check for uncommitted changes
  - [ ] Check disk space available (>500MB)
  - [ ] Check internet connection to GitHub
  - [ ] Return validation results to frontend

- [ ] **Frontend Validation Display**
  - [ ] Show validation results before update
  - [ ] Block update if validation fails
  - [ ] Show clear error messages for each failure

### Rollback System

- [ ] **Implement Rollback Endpoint**
  - [ ] Add `POST /api/updates/rollback`
  - [ ] Find latest backup
  - [ ] Restore workspace and .secrets
  - [ ] Checkout previous Git commit
  - [ ] Restart services

- [ ] **Frontend Rollback UI**
  - [ ] Add "Rollback" button (shown after failed update)
  - [ ] Confirm before rollback
  - [ ] Show rollback progress

### Error Handling

- [ ] **Improve Error Messages**
  - [ ] Git pull failed → "Unable to pull latest code. Check internet connection."
  - [ ] Pip install failed → "Dependency installation failed. See logs."
  - [ ] NPM build failed → "Frontend build failed. Rolling back..."
  - [ ] Service restart failed → "Services failed to restart. Manual intervention needed."

- [ ] **Add Logging**
  - [ ] Log all update steps to `update.log`
  - [ ] Include timestamps
  - [ ] Include error details
  - [ ] Make log accessible via API

### Testing

- [ ] **Test Failure Scenarios**
  - [ ] No internet connection
  - [ ] Git not installed
  - [ ] Uncommitted changes in repo
  - [ ] Insufficient disk space
  - [ ] Dependency installation fails
  - [ ] Service restart fails

- [ ] **Test Rollback**
  - [ ] Trigger failed update
  - [ ] Verify rollback button appears
  - [ ] Click rollback
  - [ ] Verify previous version restored
  - [ ] Verify workspace intact

---

## 📋 Phase 3: User Experience (Nice to Have)

### Release Notes

- [ ] **Display Release Notes**
  - [ ] Fetch from GitHub API (`release.body`)
  - [ ] Parse markdown to HTML
  - [ ] Show in expandable section
  - [ ] Add "What's New" icon

### Update Scheduling

- [ ] **Allow Deferred Updates**
  - [ ] Add "Remind Me Later" button
  - [ ] Store in localStorage
  - [ ] Show reminder on next launch
  - [ ] Add "Schedule for next restart" option

### Update Caching

- [ ] **Cache Update Check Results**
  - [ ] Cache for 24 hours
  - [ ] Add force refresh option
  - [ ] Show "Last checked: X hours ago"

### Progress Visualization

- [ ] **Enhanced Progress UI**
  - [ ] Add progress bar (0-100%)
  - [ ] Show current step (1/5)
  - [ ] Estimated time remaining
  - [ ] Animated icons for each step

### Notifications

- [ ] **Desktop Notifications**
  - [ ] Notify when update available
  - [ ] Notify when update complete
  - [ ] Notify if update failed

---

## 📋 Documentation

- [ ] **Update README.md**
  - [ ] Add "Updating" section
  - [ ] Explain auto-update feature
  - [ ] Document manual update process
  - [ ] Add troubleshooting section

- [ ] **Update USER_MANUAL.md**
  - [ ] Add update instructions
  - [ ] Add screenshots of update banner
  - [ ] Explain what gets updated vs preserved

- [ ] **Update UPDATE_GUIDE.md**
  - [ ] Document new Git-based approach
  - [ ] Update developer release process
  - [ ] Add rollback instructions

- [ ] **Create TROUBLESHOOTING.md**
  - [ ] Common update issues
  - [ ] How to check update.log
  - [ ] How to manually rollback
  - [ ] How to force update

---

## 📋 Release Process

### Prepare for v1.1.0 Release

- [ ] **Update VERSION File**
  - [ ] Change from `1.0.0` to `1.1.0`
  - [ ] Commit change

- [ ] **Add Visible Changes**
  - [ ] Add new sample model (e.g., Weather)
  - [ ] Change theme color (e.g., blue → purple)
  - [ ] Update something in UI

- [ ] **Build Package**
  - [ ] Run `./create-package.sh`
  - [ ] Verify package created
  - [ ] Test package locally

- [ ] **Create Git Tag**
  - [ ] `git tag v1.1.0`
  - [ ] `git push origin v1.1.0`

- [ ] **Create GitHub Release**
  - [ ] Go to GitHub releases page
  - [ ] Click "Create new release"
  - [ ] Tag: `v1.1.0`
  - [ ] Title: "AIP Notebook v1.1.0 - Auto-Update Improvements"
  - [ ] Description: List changes
  - [ ] Upload: `AIP-Model-Builder-Installer.tar.gz`
  - [ ] Publish release

### Test Update Flow

- [ ] **Install v1.0.0**
  - [ ] Extract installer
  - [ ] Run installation
  - [ ] Verify app works

- [ ] **Trigger Update**
  - [ ] Launch app
  - [ ] Wait for update banner
  - [ ] Click "Update Now"
  - [ ] Monitor progress

- [ ] **Verify Update Success**
  - [ ] App restarts automatically
  - [ ] Version shows v1.1.0
  - [ ] New features visible
  - [ ] Workspace preserved
  - [ ] No errors in console

---

## 📋 Code Review Checklist

### Before Merging

- [ ] **Code Quality**
  - [ ] No hardcoded paths
  - [ ] Proper error handling
  - [ ] Logging added
  - [ ] Comments for complex logic
  - [ ] Type hints (Python)
  - [ ] PropTypes (React)

- [ ] **Security**
  - [ ] No secrets in code
  - [ ] HTTPS for GitHub API
  - [ ] User confirmation required
  - [ ] Backup before destructive operations
  - [ ] Input validation

- [ ] **Testing**
  - [ ] Unit tests added
  - [ ] Integration tests pass
  - [ ] Manual testing on all platforms
  - [ ] Edge cases covered

- [ ] **Documentation**
  - [ ] README updated
  - [ ] API docs updated
  - [ ] Comments added
  - [ ] Changelog updated

---

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] **Version Bump**
  - [ ] Update VERSION file
  - [ ] Update package.json version
  - [ ] Update any hardcoded versions

- [ ] **Build & Test**
  - [ ] Run tests
  - [ ] Build frontend
  - [ ] Create package
  - [ ] Test package installation

- [ ] **Documentation**
  - [ ] Update CHANGELOG.md
  - [ ] Update release notes
  - [ ] Update screenshots if UI changed

### Deployment

- [ ] **Git Operations**
  - [ ] Commit all changes
  - [ ] Push to main
  - [ ] Create tag
  - [ ] Push tag

- [ ] **GitHub Release**
  - [ ] Create release
  - [ ] Upload installer
  - [ ] Publish

### Post-Deployment

- [ ] **Verification**
  - [ ] Test update from previous version
  - [ ] Check GitHub API returns correct version
  - [ ] Verify download link works
  - [ ] Test on fresh installation

- [ ] **Monitoring**
  - [ ] Monitor for user issues
  - [ ] Check error logs
  - [ ] Respond to bug reports

---

## 📋 Quick Reference

### Files to Modify

```
backend/
  routes/
    updates.py          ← Main update logic
  scripts/
    update-unix.sh      ← New: Unix update script
    update-windows.ps1  ← New: Windows update script

frontend/
  src/
    App.jsx            ← Update UI and version display

VERSION                ← Bump on each release

README.md              ← Document update feature
UPDATE_GUIDE.md        ← Update with new process
```

### Key Functions to Implement

```python
# backend/routes/updates.py

def validate_update_prerequisites() -> dict
def create_backup(app_dir: Path) -> Path
def generate_update_script(platform: str) -> str
def execute_update_script(script: str) -> None

@router.get("/validate")
@router.get("/status")
@router.post("/perform")
@router.post("/rollback")
```

```javascript
// frontend/src/App.jsx

const fetchCurrentVersion = async () => { }
const performUpdate = async () => { }
const pollUpdateStatus = async () => { }
const handleRollback = async () => { }
```

---

## 📋 Success Criteria

### Update is successful if:

- [x] User sees update banner within 5 seconds of new release
- [x] Update completes in under 2 minutes
- [x] App restarts automatically
- [x] User workspace is preserved
- [x] User .secrets are preserved
- [x] New version is running
- [x] No errors in console
- [x] Works on Windows (WSL), Mac, and Linux

### Update is robust if:

- [x] Validation prevents updates when prerequisites not met
- [x] Backup is created before update
- [x] Rollback works if update fails
- [x] Clear error messages shown
- [x] Update log is accessible
- [x] User data never lost

---

## 🎯 Next Steps

1. **Review Specification**
   - Read `AUTO_UPDATE_SPECIFICATION.md`
   - Read `AUTO_UPDATE_SUMMARY.md`
   - Review `AUTO_UPDATE_FLOWS.md`

2. **Start Implementation**
   - Begin with Phase 1 (Core Functionality)
   - Test thoroughly on WSL
   - Move to Phase 2 (Safety)

3. **Create Test Release**
   - Make v1.0.1 with small visible change
   - Test update flow end-to-end
   - Fix any issues

4. **Deploy to Production**
   - Create v1.1.0 with full auto-update feature
   - Monitor for issues
   - Iterate based on feedback

---

**Good luck! 🚀**
