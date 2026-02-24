# ⭐ START HERE - Complete Setup Guide

Welcome to the Grievance Hub application! This document will guide you through everything you need to know.

---

## 📂 What You Have

A fully restructured Grievance Hub application with:
- **Backend:** Flask REST API with SQLAlchemy ORM
- **Frontend:** Vanilla HTML/CSS/JavaScript (no build process)
- **Database:** SQLite with 9 tables
- **Models:** Pre-trained ML models for complaint classification
- **Docs:** Complete documentation for setup and deployment

---

## 🚀 5-Minute Quick Start

### Prerequisites
- Python 3.8+ installed
- Internet connection (first time only, to download dependencies)

### Step 1: Start Backend

Open Terminal/Command Prompt and run:

```bash
cd backend
python -m venv venv
source venv/bin/activate     # macOS/Linux
# OR
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python run.py
```

**Wait for this message:**
```
Running on http://127.0.0.1:5000
```

### Step 2: Start Frontend

Open a NEW terminal and run:

```bash
cd frontend
python -m http.server 8000
```

**Wait for this message:**
```
Serving HTTP on 0.0.0.0 port 8000
```

### Step 3: Open Browser

Go to: **http://localhost:8000**

✅ Done! Application is live!

---

## 📁 Project Structure at a Glance

```
Your Project Folder/
│
├── backend/                    ← Flask REST API Server
│   ├── app/
│   │   ├── __init__.py        ← App initialization
│   │   ├── models.py          ← Database models
│   │   ├── utils.py           ← Helper functions
│   │   └── routes/            ← API endpoints
│   ├── scripts/
│   │   └── seed_db.py         ← Create demo data
│   ├── run.py                 ← START HERE: python run.py
│   └── requirements.txt        ← Python libraries
│
├── frontend/                   ← Web Pages
│   ├── *.html                 ← 5 web pages
│   ├── css/style.css          ← All styling
│   └── js/                    ← Page logic
│
├── data/                       ← Database (created at runtime)
├── models/                     ← ML models
├── public/                     ← Images & assets
│
└── Documentation:
    ├── README.md              ← Project overview
    ├── SETUP.md               ← Detailed setup
    ├── QUICKSTART.md          ← Quick start (this)
    ├── FOLDER_STRUCTURE.md    ← Complete file guide
    ├── ARCHITECTURE.txt       ← System architecture
    └── PROJECT_TREE.txt       ← ASCII folder tree
```

**Key Folders:**
- `backend/` - Copy this entire folder
- `frontend/` - Copy this entire folder
- `data/` - Will be created automatically
- `models/` - Copy this entire folder

---

## 🔐 Login Credentials

After starting the backend (which creates demo data), use these to log in:

**Super Admin:**
- Email: `superadmin@grievancehub.com`
- Password: `SuperAdmin@123`

**Sub Admin:**
- Email: `subadmin_zone1@grievancehub.com`
- Password: `SubAdmin@123`

**Department Admin:**
- Email: `deptadmin_circle1@grievancehub.com`
- Password: `DeptAdmin@123`

---

## 📍 URLs to Access

| Page | URL |
|------|-----|
| Home | http://localhost:8000 |
| Submit Complaint | http://localhost:8000/submit-complaint.html |
| Track Complaint | http://localhost:8000/track-complaint.html |
| Admin Login | http://localhost:8000/admin-login.html |
| Admin Dashboard | http://localhost:8000/admin-dashboard.html |
| Backend API | http://localhost:5000/api/... |

---

## 📋 Complete File Checklist

### Backend Files (Must Include)

```
✅ backend/
   ├── app/
   │   ├── __init__.py
   │   ├── models.py
   │   ├── utils.py
   │   ├── routes/
   │   │   ├── __init__.py
   │   │   ├── auth_routes.py
   │   │   ├── complaint_routes.py
   │   │   ├── admin_routes.py
   │   │   └── zone_routes.py
   │   └── (rest of files)
   ├── scripts/
   │   ├── __init__.py
   │   └── seed_db.py
   ├── run.py
   ├── requirements.txt
   └── .env.example
```

### Frontend Files (Must Include)

```
✅ frontend/
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
```

### Data & Models (Must Include)

```
✅ data/                    (empty folder, created at runtime)
✅ models/                  (all .pkl files)
✅ public/                  (images and assets)
```

---

## 🛠️ Step-by-Step Setup (Detailed)

### Step 1: Prepare Your Machine

Ensure you have:
- Python 3.8 or newer: `python --version`
- Git (optional): `git --version`

If you don't have Python, download from [python.org](https://www.python.org/downloads/)

### Step 2: Extract Files

1. Copy the entire project folder to your desired location
2. Open Terminal/Command Prompt
3. Navigate to project folder: `cd path/to/grievance-hub`

### Step 3: Setup Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment (isolated Python environment)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install all required Python packages
pip install -r requirements.txt

# (Optional) Create .env file for configuration
cp .env.example .env

# Seed database with demo data
python scripts/seed_db.py
# This creates data/grievance.db with tables and demo data

# Start the server
python run.py
# Should show: Running on http://127.0.0.1:5000
```

### Step 4: Setup Frontend

Open a NEW terminal window:

```bash
# Navigate to frontend folder
cd frontend

# Start web server
python -m http.server 8000
# Should show: Serving HTTP on 0.0.0.0 port 8000
```

### Step 5: Access Application

1. Open your web browser
2. Go to: `http://localhost:8000`
3. Try submitting a complaint or logging in as admin

---

## 📊 What Each Component Does

### Backend (Python/Flask)

**`app/__init__.py`** - Creates Flask application
- Initializes database connection
- Registers API routes
- Configures CORS for frontend

**`app/models.py`** - Database models (SQLAlchemy ORM)
- Defines Users table
- Defines Complaints table
- Defines Admins, AdminSessions, Zones, Circles, Areas tables
- Defines relationships between tables

**`app/utils.py`** - Utility functions
- `generate_otp()` - Creates one-time passwords
- `send_email()` - Sends emails via SMTP
- `classify_complaint()` - AI classification of complaints
- `validate_phone()` - Phone number validation

**`app/routes/*.py`** - API endpoints
- `auth_routes.py` - Login, OTP, logout
- `complaint_routes.py` - Submit, track, update complaints
- `admin_routes.py` - Dashboard, analytics, management
- `zone_routes.py` - Geographic data

**`run.py`** - Main entry point
- Starts Flask server on port 5000

**`scripts/seed_db.py`** - Database initialization
- Creates tables
- Inserts demo zones, circles, areas
- Inserts demo admin accounts
- Inserts sample complaints

### Frontend (HTML/CSS/JavaScript)

**HTML Files** - Web pages
- `index.html` - Home page with navigation
- `submit-complaint.html` - Complaint submission form
- `track-complaint.html` - Track complaint status
- `admin-login.html` - Admin login page
- `admin-dashboard.html` - Admin panel with analytics

**`css/style.css`** - Styling for all pages
- Responsive design (mobile, tablet, desktop)
- Light/dark theme colors
- Form styling
- Dashboard components

**`js/` files** - Page logic
- `config.js` - API endpoints and constants
- `submit-complaint.js` - Form handling
- `track-complaint.js` - Search and display
- `admin-login.js` - Authentication
- `admin-dashboard.js` - Dashboard rendering

---

## 🔗 API Endpoints Reference

### Authentication
```
POST   /api/auth/login              - Login with email
POST   /api/auth/verify-otp         - Verify OTP
POST   /api/auth/logout             - Logout
GET    /api/auth/user               - Get current user
```

### Complaints
```
POST   /api/complaints              - Submit new complaint
GET    /api/complaints              - List all complaints (with filters)
GET    /api/complaints/<id>         - Get specific complaint
GET    /api/complaints/<id>/status  - Get complaint status
PUT    /api/complaints/<id>/status  - Update complaint status
DELETE /api/complaints/<id>         - Delete complaint
```

### Admin
```
GET    /api/admin/dashboard         - Dashboard statistics
GET    /api/admin/analytics         - Analytics data
GET    /api/admin/complaints        - Complaint list with pagination
```

### Geographic Data
```
GET    /api/zones                   - Get all zones
GET    /api/zones/<id>/circles      - Get circles in zone
GET    /api/circles/<id>/areas      - Get areas in circle
```

---

## ❓ Troubleshooting

### Problem: "Python command not found"
**Solution:** Install Python from [python.org](https://www.python.org/downloads/)

### Problem: "Module not found" error
**Solution:** Make sure virtual environment is activated and pip install was successful
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Problem: "Port 5000 is already in use"
**Solution:** Either stop the process using port 5000 or change port in `backend/run.py`
```python
# In backend/run.py, change:
app.run(debug=True, port=5000)
# To:
app.run(debug=True, port=5001)
```

### Problem: "Frontend can't reach backend"
**Solution:** Ensure backend is running AND check config.js
```javascript
// In frontend/js/config.js, verify:
const API_BASE_URL = 'http://localhost:5000';
```

### Problem: "Database error when loading admin dashboard"
**Solution:** Delete old database and reseed
```bash
cd backend
rm data/grievance.db          # macOS/Linux
del data\grievance.db         # Windows
python scripts/seed_db.py     # Recreate database
python run.py                 # Restart server
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `START_HERE.md` | This file - quick start |
| `README.md` | Project overview & features |
| `SETUP.md` | Detailed setup instructions |
| `QUICKSTART.md` | 5-minute quick start |
| `FOLDER_STRUCTURE.md` | Complete folder reference |
| `ARCHITECTURE.txt` | System architecture & diagrams |
| `PROJECT_TREE.txt` | ASCII folder tree view |
| `FILE_MANIFEST.md` | Complete file descriptions |
| `QUICK_REFERENCE.md` | Quick lookup guide |
| `MIGRATION_CHECKLIST.md` | Verification checklist |

**Recommended reading order:**
1. START_HERE.md (this file)
2. QUICKSTART.md (5 min setup)
3. FOLDER_STRUCTURE.md (understand structure)
4. ARCHITECTURE.txt (understand system)

---

## ✨ Key Features

### User Features
✅ Submit complaints with AI-based category classification
✅ Track complaint status with real-time updates
✅ Email notifications for status changes
✅ OTP-based verification
✅ Location-based complaint routing
✅ Multi-language support

### Admin Features
✅ Role-based access (Super Admin, Sub Admin, Dept Admin)
✅ Dashboard with statistics
✅ Analytics and graphs
✅ Complaint management interface
✅ Advanced filtering and search
✅ Status update and assignment
✅ Session-based authentication

### Technical Features
✅ RESTful API architecture
✅ SQLAlchemy ORM (no raw SQL)
✅ Responsive design (mobile/tablet/desktop)
✅ No frontend build process needed
✅ Pre-trained ML models
✅ Email integration
✅ Database relationships and constraints

---

## 🎯 Next Steps

1. **Follow the 5-Minute Quick Start** above
2. **Test the application:**
   - Submit a test complaint
   - Log in as admin
   - View analytics
3. **Explore the code:**
   - Read `ARCHITECTURE.txt` for system design
   - Review `backend/app/models.py` for database
   - Check `frontend/js/` for API calls
4. **Read documentation:**
   - All docs are in the root folder
   - Start with `FOLDER_STRUCTURE.md`
5. **Deploy to production:**
   - Use `SETUP.md` deployment section
   - Or use `README.md` for cloud deployment

---

## 📞 Need Help?

1. **Check the error message** - it usually tells you what's wrong
2. **See Troubleshooting section** above
3. **Read SETUP.md** for detailed instructions
4. **Read ARCHITECTURE.txt** for system understanding
5. **Check FILE_MANIFEST.md** for file descriptions

---

## ✅ You're All Set!

You have everything needed to run the Grievance Hub application. Follow the 5-Minute Quick Start above and you'll have a working application in minutes.

**Start with:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Then in another terminal:
```bash
cd frontend
python -m http.server 8000
```

Then open: **http://localhost:8000**

Enjoy! 🎉

