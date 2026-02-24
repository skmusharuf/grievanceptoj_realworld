# Quick Reference Guide

## What to Include in Your Project

### Main Folders to Copy:

1. **backend/** - Flask REST API server
2. **frontend/** - HTML/CSS/JavaScript pages
3. **data/** - Database and configuration
4. **models/** - Machine Learning models
5. **public/** - Static assets (logos, images)

### Key Files to Copy:

**Root Level:**
- `README.md` - Project documentation
- `SETUP.md` - Setup instructions
- `QUICKSTART.md` - Quick start guide
- `FOLDER_STRUCTURE.md` - This folder guide
- `PROJECT_TREE.txt` - ASCII tree view
- `QUICK_REFERENCE.md` - This file

---

## Complete Directory Listing

### What to Include (REQUIRED)

```
✅ backend/                    # Flask application
   ├── app/
   │   ├── __init__.py
   │   ├── models.py
   │   ├── utils.py
   │   └── routes/
   │       ├── auth_routes.py
   │       ├── complaint_routes.py
   │       ├── admin_routes.py
   │       └── zone_routes.py
   ├── scripts/
   │   └── seed_db.py
   ├── run.py
   ├── requirements.txt
   └── .env.example

✅ frontend/                   # Web pages
   ├── index.html
   ├── submit-complaint.html
   ├── track-complaint.html
   ├── admin-login.html
   ├── admin-dashboard.html
   ├── css/
   │   └── style.css
   └── js/
       ├── config.js
       ├── submit-complaint.js
       ├── track-complaint.js
       ├── admin-login.js
       └── admin-dashboard.js

✅ models/                     # ML Models (all .pkl files)
✅ public/                     # Images & assets
✅ data/                       # Database (created at runtime)

✅ Documentation:
   ├── README.md
   ├── SETUP.md
   ├── QUICKSTART.md
   ├── FOLDER_STRUCTURE.md
   └── PROJECT_TREE.txt
```

### What NOT to Include (Legacy/Optional)

```
❌ app/                        # Old Next.js (BEING REPLACED)
❌ components/                 # Old React components (BEING REPLACED)
❌ hooks/                      # Old React hooks (BEING REPLACED)
❌ lib/                        # Old utilities (BEING REPLACED)
❌ styles/                     # Old CSS (BEING REPLACED)
❌ scripts/app2createdinfeb.py # Old monolithic file (BEING REPLACED)
❌ package.json               # Old Node setup (BEING REPLACED)
❌ tsconfig.json              # Old TypeScript (BEING REPLACED)
❌ next.config.mjs            # Old Next.js config (BEING REPLACED)
```

---

## Minimal File Structure You Need

If you want just the working application, here's the minimum:

```
my-grievance-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── utils.py
│   │   └── routes/
│   │       ├── auth_routes.py
│   │       ├── complaint_routes.py
│   │       ├── admin_routes.py
│   │       └── zone_routes.py
│   ├── scripts/
│   │   └── seed_db.py
│   ├── run.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── submit-complaint.html
│   ├── track-complaint.html
│   ├── admin-login.html
│   ├── admin-dashboard.html
│   ├── css/style.css
│   └── js/
│       ├── config.js
│       ├── submit-complaint.js
│       ├── track-complaint.js
│       ├── admin-login.js
│       └── admin-dashboard.js
│
├── data/                      # Empty folder, created at runtime
├── models/                    # All .pkl files from original
├── public/                    # Images and assets
├── README.md
└── SETUP.md
```

---

## 5-Minute Setup

### Step 1: Navigate to Project
```bash
cd grievanceptoj_realworld
```

### Step 2: Terminal 1 - Start Backend
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python run.py
```

Expected output:
```
Running on http://127.0.0.1:5000
```

### Step 3: Terminal 2 - Start Frontend
```bash
cd frontend
python -m http.server 8000
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 8000
```

### Step 4: Open Browser
```
http://localhost:8000
```

Done! Application is running.

---

## Complete File Count

| Category | Count | Type |
|----------|-------|------|
| Backend Python Files | 10 | .py |
| Frontend HTML Files | 5 | .html |
| Frontend CSS Files | 1 | .css |
| Frontend JS Files | 5 | .js |
| ML Models | 8+ | .pkl |
| Documentation | 7 | .md |
| **TOTAL** | **~40** | **Mixed** |

---

## File Purposes Quick Reference

### Backend Files

| File | What It Does |
|------|------|
| `app/__init__.py` | Creates Flask app, sets up database |
| `app/models.py` | Defines database tables (Users, Complaints, Admins, etc.) |
| `app/utils.py` | Email, OTP, AI classification functions |
| `auth_routes.py` | Login, OTP verification endpoints |
| `complaint_routes.py` | Submit, track, update complaint endpoints |
| `admin_routes.py` | Dashboard, analytics, complaint management |
| `zone_routes.py` | Geographic data endpoints |
| `run.py` | Starts the Flask server |
| `seed_db.py` | Creates demo data in database |
| `requirements.txt` | List of Python libraries needed |

### Frontend Files

| File | What It Does |
|------|------|
| `index.html` | Home page with navigation |
| `submit-complaint.html` | Form to submit new complaints |
| `track-complaint.html` | Search and view complaint status |
| `admin-login.html` | Admin login form |
| `admin-dashboard.html` | Admin analytics and management panel |
| `style.css` | All styling for all pages |
| `config.js` | API endpoints and utilities |
| `submit-complaint.js` | Handles form submission logic |
| `track-complaint.js` | Handles complaint tracking |
| `admin-login.js` | Handles admin authentication |
| `admin-dashboard.js` | Renders dashboard with charts |

---

## Running Each Component

### Backend Commands

```bash
# Navigate to backend
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate it
source venv/bin/activate        # macOS/Linux
# or
venv\Scripts\activate           # Windows

# Install dependencies (first time only)
pip install -r requirements.txt

# Seed database with demo data (first time only)
python scripts/seed_db.py

# Start backend server
python run.py
```

### Frontend Commands

```bash
# Navigate to frontend
cd frontend

# Start simple web server
python -m http.server 8000
```

### Access Application

- Home: `http://localhost:8000`
- Submit: `http://localhost:8000/submit-complaint.html`
- Track: `http://localhost:8000/track-complaint.html`
- Admin: `http://localhost:8000/admin-login.html`

---

## Important Notes

1. **Ports Used:**
   - Backend: 5000
   - Frontend: 8000

2. **Database:**
   - Created automatically in `data/grievance.db`
   - Uses SQLite
   - Demo data added by `seed_db.py`

3. **No Build Process:**
   - Frontend is plain HTML/CSS/JS
   - No compilation needed
   - Just serve the folder

4. **Demo Accounts:**
   - Email: `superadmin@grievancehub.com`
   - Password: `SuperAdmin@123`
   - (See FOLDER_STRUCTURE.md for more accounts)

5. **Configuration:**
   - Optional `.env` file in backend folder
   - Defaults work without .env

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python 3.8+ |
| "Port 5000 in use" | Kill process or use different port |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Database error" | Delete `data/grievance.db` and rerun seed_db.py |
| "Frontend can't reach backend" | Ensure backend is running on 5000 |

---

## Next Steps

1. **Copy all required folders** to your machine
2. **Follow the 5-Minute Setup** above
3. **Read SETUP.md** for detailed instructions
4. **Check FOLDER_STRUCTURE.md** for complete reference
5. **View PROJECT_TREE.txt** for visual layout

All documentation is in the root folder!

