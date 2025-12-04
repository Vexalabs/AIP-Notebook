# Auto-Update System - Flow Diagrams

## Current Implementation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER OPENS APPLICATION                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Frontend Loads │
                    └────────┬───────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Call: GET /api/updates/check │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────────┐
              │ Backend queries GitHub API:      │
              │ /repos/Vexalabs/AIP-Notebook/    │
              │ releases/latest                  │
              └──────────────┬───────────────────┘
                             │
                             ▼
              ┌──────────────────────────────────┐
              │ Compare versions:                │
              │ Current (from VERSION file)      │
              │ vs Latest (from GitHub tag)      │
              └──────────────┬───────────────────┘
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ▼                   ▼
         ┌─────────────────┐   ┌──────────────┐
         │ Update Available│   │ Up to Date   │
         └────────┬────────┘   └──────┬───────┘
                  │                   │
                  ▼                   ▼
    ┌──────────────────────┐   ┌─────────────┐
    │ Show Update Banner   │   │ No Banner   │
    │ "v1.1.0 Available"   │   │             │
    └──────────┬───────────┘   └─────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ User Clicks          │
    │ "Update Now"         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │ Call: POST /api/updates/perform  │
    └──────────┬───────────────────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │ Backend:                         │
    │ 1. Download .tar.gz from GitHub  │
    │ 2. Extract to temp directory     │
    │ 3. Generate bash update script   │
    │ 4. Execute script with nohup     │
    └──────────┬───────────────────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │ Update Script:                   │
    │ 1. pkill uvicorn & vite          │
    │ 2. rsync files (exclude workspace)│
    │ 3. Run ./setup.sh                │
    │ 4. Start ./run.sh                │
    └──────────┬───────────────────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │ Frontend waits 10 seconds        │
    │ then reloads page                │
    └──────────────────────────────────┘
```

**Issues with Current Flow:**
- ❌ Downloads entire archive (slow, wasteful)
- ❌ Kills processes that may include itself
- ❌ No progress feedback during 10-second wait
- ❌ No validation before starting
- ❌ No backup before overwriting files

---

## Proposed Implementation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER OPENS APPLICATION                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Frontend Loads │
                    └────────┬───────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌────────────────────┐   ┌────────────────────────┐
    │ Fetch Current      │   │ Check for Updates      │
    │ Version from API   │   │ GET /api/updates/check │
    └────────┬───────────┘   └────────┬───────────────┘
             │                        │
             ▼                        ▼
    ┌────────────────────┐   ┌────────────────────────┐
    │ Display: v1.0.0    │   │ GitHub API Query       │
    │ (dynamic)          │   │ (cached for 24h)       │
    └────────────────────┘   └────────┬───────────────┘
                                      │
                            ┌─────────┴─────────┐
                            │                   │
                            ▼                   ▼
                  ┌─────────────────┐   ┌──────────────┐
                  │ Update Available│   │ Up to Date   │
                  └────────┬────────┘   └──────────────┘
                           │
                           ▼
              ┌────────────────────────────┐
              │ Show Enhanced Update Banner│
              │ - Version: v1.1.0          │
              │ - Release Notes (expandable)│
              │ - "Update Now" button      │
              └────────┬───────────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ User Clicks        │
              │ "Update Now"       │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────────────────┐
              │ Confirmation Dialog:           │
              │ "This will restart the app.    │
              │  Continue?"                    │
              └────────┬───────────────────────┘
                       │
                       ▼ (User confirms)
              ┌────────────────────────────────┐
              │ Call: GET /api/updates/validate│
              └────────┬───────────────────────┘
                       │
                       ▼
              ┌────────────────────────────────┐
              │ Pre-Update Validation:         │
              │ ✓ Git installed?               │
              │ ✓ Is Git repository?           │
              │ ✓ Internet connection?         │
              │ ✓ Disk space available?        │
              │ ✓ No uncommitted changes?      │
              └────────┬───────────────────────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
    ┌─────────────────┐   ┌──────────────────┐
    │ Validation PASS │   │ Validation FAIL  │
    └────────┬────────┘   └────────┬─────────┘
             │                     │
             │                     ▼
             │            ┌─────────────────────┐
             │            │ Show Error Message  │
             │            │ "Git not installed" │
             │            └─────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ Call: POST /api/updates/perform│
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ Backend:                       │
    │ 1. Create backup               │
    │    - workspace/                │
    │    - .secrets/                 │
    │    - VERSION                   │
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ 2. Generate Update Script:     │
    │    - git pull origin main      │
    │    - pip install -r requirements│
    │    - npm install && build      │
    │    - restart services          │
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ 3. Execute script in background│
    │    (detached process)          │
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ Frontend: Poll for Status      │
    │ GET /api/updates/status        │
    │ Every 2 seconds                │
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ Show Progress:                 │
    │ ⏳ "Pulling latest code..."    │
    │ ⏳ "Installing dependencies..." │
    │ ⏳ "Building frontend..."       │
    │ ⏳ "Restarting services..."     │
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ Update Complete!               │
    │ ✅ "Update successful"          │
    │    Auto-reload in 3 seconds... │
    └────────┬───────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ Page Reloads                   │
    │ New version running!           │
    └────────────────────────────────┘
```

---

## Update Script Execution Flow

```
┌─────────────────────────────────────┐
│  Update Script Starts               │
│  (Detached from main process)       │
└──────────────┬──────────────────────┘
               │
               ▼
      ┌────────────────────┐
      │ Log: "Starting..." │
      │ → update.log       │
      └────────┬───────────┘
               │
               ▼
      ┌────────────────────────┐
      │ Stop Running Services: │
      │ pkill -f uvicorn       │
      │ pkill -f vite          │
      └────────┬───────────────┘
               │
               ▼
      ┌────────────────────────┐
      │ Git Operations:        │
      │ git stash              │
      │ git fetch origin main  │
      │ git pull origin main   │
      └────────┬───────────────┘
               │
               ▼
      ┌────────────────────────┐
      │ Update Backend:        │
      │ source venv/bin/activate│
      │ pip install -r         │
      │   requirements.txt     │
      └────────┬───────────────┘
               │
               ▼
      ┌────────────────────────┐
      │ Update Frontend:       │
      │ cd frontend            │
      │ npm install            │
      │ npm run build          │
      └────────┬───────────────┘
               │
               ▼
      ┌────────────────────────┐
      │ Restart Application:   │
      │ nohup ./run.sh &       │
      └────────┬───────────────┘
               │
               ▼
      ┌────────────────────────┐
      │ Log: "Complete!"       │
      │ → update.log           │
      └────────────────────────┘
```

---

## Error Handling Flow

```
                    ┌─────────────────┐
                    │ Update Initiated│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Try Update      │
                    └────────┬────────┘
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ▼                   ▼
         ┌─────────────────┐   ┌──────────────┐
         │ Success         │   │ Error        │
         └────────┬────────┘   └──────┬───────┘
                  │                   │
                  ▼                   ▼
    ┌──────────────────────┐   ┌─────────────────────┐
    │ Show Success Message │   │ Log Error           │
    │ Reload App           │   │ Notify User         │
    └──────────────────────┘   └──────┬──────────────┘
                                      │
                                      ▼
                            ┌──────────────────────┐
                            │ Offer Rollback:      │
                            │ "Update failed.      │
                            │  Restore previous    │
                            │  version?"           │
                            └──────┬───────────────┘
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
              ┌──────────────────┐   ┌──────────────┐
              │ User Accepts     │   │ User Declines│
              └──────┬───────────┘   └──────────────┘
                     │
                     ▼
              ┌──────────────────────┐
              │ POST /api/updates/   │
              │      rollback        │
              └──────┬───────────────┘
                     │
                     ▼
              ┌──────────────────────┐
              │ Restore from Backup: │
              │ - Copy workspace     │
              │ - Copy .secrets      │
              │ - git checkout TAG   │
              │ - Restart            │
              └──────┬───────────────┘
                     │
                     ▼
              ┌──────────────────────┐
              │ App Running on       │
              │ Previous Version     │
              └──────────────────────┘
```

---

## Platform-Specific Execution

### Windows (WSL)

```
┌──────────────────────────┐
│ User Clicks "Update Now" │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Backend generates:           │
│ update-windows.ps1           │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Execute via PowerShell:      │
│ wsl -d Ubuntu bash -c        │
│   "cd ~/MLModelBuilder &&    │
│    git pull origin main"     │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ WSL executes Git commands    │
│ inside Ubuntu environment    │
└──────────────────────────────┘
```

### Mac/Linux

```
┌──────────────────────────┐
│ User Clicks "Update Now" │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Backend generates:           │
│ update-unix.sh               │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Execute directly:            │
│ bash update-unix.sh          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Native shell executes        │
│ Git commands                 │
└──────────────────────────────┘
```

---

## State Diagram

```
                    ┌──────────────┐
                    │   IDLE       │
                    │ (No Update)  │
                    └──────┬───────┘
                           │
                           │ Check for updates
                           │ (on app start)
                           │
                           ▼
                    ┌──────────────┐
                    │  CHECKING    │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
    ┌──────────────────┐      ┌─────────────────┐
    │ UPDATE_AVAILABLE │      │  UP_TO_DATE     │
    └──────┬───────────┘      └─────────────────┘
           │                           │
           │ User clicks               │
           │ "Update Now"              │
           │                           │
           ▼                           │
    ┌──────────────────┐              │
    │   VALIDATING     │              │
    └──────┬───────────┘              │
           │                           │
  ┌────────┴────────┐                 │
  │                 │                 │
  ▼                 ▼                 │
┌──────┐      ┌──────────┐           │
│ FAIL │      │   PASS   │           │
└──┬───┘      └────┬─────┘           │
   │               │                 │
   │               ▼                 │
   │        ┌──────────────┐         │
   │        │  UPDATING    │         │
   │        └──────┬───────┘         │
   │               │                 │
   │      ┌────────┴────────┐        │
   │      │                 │        │
   │      ▼                 ▼        │
   │  ┌─────────┐    ┌──────────┐   │
   │  │ SUCCESS │    │  ERROR   │   │
   │  └────┬────┘    └────┬─────┘   │
   │       │              │          │
   │       │              ▼          │
   │       │      ┌──────────────┐   │
   │       │      │  ROLLBACK    │   │
   │       │      └──────┬───────┘   │
   │       │             │           │
   │       ▼             ▼           ▼
   └────► ┌─────────────────────────┐
          │   IDLE (Restart App)    │
          └─────────────────────────┘
```

---

## Data Flow

```
┌─────────────┐
│   GitHub    │
│  Repository │
└──────┬──────┘
       │
       │ 1. Check latest release
       │    GET /repos/.../releases/latest
       │
       ▼
┌──────────────┐      2. Version info     ┌──────────────┐
│   Backend    │◄─────────────────────────│   Frontend   │
│   (FastAPI)  │                          │   (React)    │
└──────┬───────┘                          └──────────────┘
       │                                          ▲
       │ 3. If update needed:                     │
       │    - Create backup                       │
       │    - Generate script                     │
       │    - Execute update                      │
       │                                          │
       ▼                                          │
┌──────────────┐                                 │
│  Git Repo    │                                 │
│  (Local)     │                                 │
└──────┬───────┘                                 │
       │                                          │
       │ 4. git pull origin main                 │
       │                                          │
       ▼                                          │
┌──────────────┐                                 │
│  Updated     │                                 │
│  Code        │                                 │
└──────┬───────┘                                 │
       │                                          │
       │ 5. Restart services                     │
       │                                          │
       └──────────────────────────────────────────┘
          6. Frontend reloads, sees new version
```

---

## Timeline (Typical Update)

```
T+0s    │ User clicks "Update Now"
        │ ├─ Validation starts
        │
T+1s    │ ├─ Validation complete ✓
        │ ├─ Backup created ✓
        │ ├─ Update script generated ✓
        │ └─ Script execution started
        │
T+2s    │ ├─ Services stopped
        │ └─ Git pull started
        │
T+5s    │ ├─ Git pull complete ✓
        │ └─ Pip install started
        │
T+15s   │ ├─ Pip install complete ✓
        │ └─ NPM install started
        │
T+30s   │ ├─ NPM install complete ✓
        │ └─ NPM build started
        │
T+45s   │ ├─ NPM build complete ✓
        │ └─ Services restarting
        │
T+50s   │ ├─ Backend online ✓
        │ └─ Frontend online ✓
        │
T+52s   │ └─ Page reloads
        │     New version running! 🎉
```

**Total Time: ~50-60 seconds**

---

## Comparison: Current vs Proposed

| Aspect | Current | Proposed |
|--------|---------|----------|
| **Method** | Download .tar.gz | `git pull` |
| **Speed** | ~2-3 minutes | ~50-60 seconds |
| **Bandwidth** | ~50-100 MB | ~1-5 MB (delta) |
| **Validation** | None | Pre-flight checks |
| **Backup** | None | Automatic |
| **Rollback** | Manual | One-click |
| **Progress** | "Wait 10 seconds" | Real-time updates |
| **Platform** | Linux/WSL only | All platforms |
| **User Feedback** | Minimal | Detailed |
| **Error Handling** | Basic | Comprehensive |

---

See `AUTO_UPDATE_SPECIFICATION.md` for complete implementation details.
