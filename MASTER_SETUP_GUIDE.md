# 🎯 MASTER SETUP GUIDE - GRIEVANCE HUB

> **Read this document first. This is your complete guide to set up and run the project.**

---

## 📋 TABLE OF CONTENTS

1. [What You Have](#what-you-have)
2. [Exact Folder Structure](#exact-folder-structure)
3. [All Files to Copy](#all-files-to-copy)
4. [Setup Instructions](#setup-instructions)
5. [How to Run](#how-to-run)
6. [Test the Application](#test-the-application)
7. [Troubleshooting](#troubleshooting)

---

## 🎁 What You Have

A complete, production-ready Grievance Hub application with:

- ✅ **Backend**: Flask REST API (Python)
- ✅ **Frontend**: HTML/CSS/JavaScript (No build process)
- ✅ **Database**: SQLite (Auto-created)
- ✅ **ML Models**: Pre-trained complaint classifiers
- ✅ **Documentation**: Complete guides

**Total Size**: ~8,000 lines of code + documentation

---

## 📁 EXACT FOLDER STRUCTURE

Copy and create this structure in your project folder:

```
your-project-folder/
│
├── 📁 backend/                           ← MAIN API SERVER
│   ├── 📁 app/
│   │   ├── __init__.py                   (FILE)
│   │   ├── models.py                     (FILE)
│   │   ├── utils.py                      (FILE)
│   │   └── 📁 routes/
│   │       ├── __init__.py               (FILE)
│   │       ├── auth_routes.py            (FILE)
│   │       ├── complaint_routes.py       (FILE)
│   │       ├── admin_routes.py           (FILE)
│   │       └── zone_routes.py            (FILE)
│   ├── 📁 scripts/
│   │   ├── __init__.py                   (FILE)
│   │   └── seed_db.py                    (FILE)
│   ├── run.py                            (FILE) ← START HERE
│   ├── requirements.txt                  (FILE)
│   └── .env.example                      (FILE)
│
├── 📁 frontend/                          ← WEB PAGES
│   ├── index.html                        (FILE - Home page)
│   ├── submit-complaint.html             (FILE)
│   ├── track-complaint.html              (FILE)
│   ├── admin-login.html                  (FILE)
│   ├── admin-dashboard.html              (FILE)
│   ├── 📁 css/
│   │   └── style.css                     (FILE)
│   └── 📁 js/
│       ├── config.js                     (FILE)
│       ├── submit-complaint.js           (FILE)
│       ├── track-complaint.js            (FILE)
│       ├── admin-login.js                (FILE)
│       └── admin-dashboard.js            (FILE)
│
├── 📁 data/                              ← DATABASE (AUTO-CREATED)
│   └── grievance_hub.db                  (CREATED AT RUNTIME)
│
├── 📁 models/                            ← ML MODELS (AUTO-CREATED)
│   └── *.pkl files                       (CREATED AT RUNTIME)
│
└── 📁 public/                            ← IMAGES
    └── images/                           (OPTIONAL)
```

---

## 📦 ALL FILES TO COPY

### Step 1: Copy Backend Files

**Location**: In your project, create the `backend/` folder

| File Path | File Content |
|-----------|--------------|
| `backend/__init__.py` | Empty file (just create it) |
| `backend/app/__init__.py` | Flask app factory |
| `backend/app/models.py` | Database models (240 lines) |
| `backend/app/utils.py` | Helper functions (200 lines) |
| `backend/app/routes/__init__.py` | Empty file |
| `backend/app/routes/auth_routes.py` | Authentication endpoints (190 lines) |
| `backend/app/routes/complaint_routes.py` | Complaint endpoints (240 lines) |
| `backend/app/routes/admin_routes.py` | Admin endpoints (270 lines) |
| `backend/app/routes/zone_routes.py` | Zone endpoints (90 lines) |
| `backend/scripts/__init__.py` | Empty file |
| `backend/scripts/seed_db.py` | Database seeding (180 lines) |
| `backend/run.py` | Main server file (40 lines) |
| `backend/requirements.txt` | Python dependencies |
| `backend/.env.example` | Environment variables template |

### Step 2: Copy Frontend Files

**Location**: In your project, create the `frontend/` folder

#### HTML Files (5 files):
| File Path | Purpose |
|-----------|---------|
| `frontend/index.html` | Home page |
| `frontend/submit-complaint.html` | Submit complaint form |
| `frontend/track-complaint.html` | Track complaint status |
| `frontend/admin-login.html` | Admin login page |
| `frontend/admin-dashboard.html` | Admin dashboard |

#### CSS File (1 file):
| File Path | Purpose |
|-----------|---------|
| `frontend/css/style.css` | All styling (934 lines) |

#### JavaScript Files (5 files):
| File Path | Purpose |
|-----------|---------|
| `frontend/js/config.js` | API configuration |
| `frontend/js/submit-complaint.js` | Submit form logic |
| `frontend/js/track-complaint.js` | Track logic |
| `frontend/js/admin-login.js` | Login logic |
| `frontend/js/admin-dashboard.js` | Dashboard logic |

---

## 🚀 SETUP INSTRUCTIONS

### Prerequisites

1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **Text Editor** - VSCode, Sublime, or any editor
3. **Terminal/Command Prompt** - Built-in to your OS

### Verification

Check if Python is installed:
```bash
python --version
# Should show: Python 3.8.x or higher
```

---

## ▶️ HOW TO RUN (Step-by-Step)

### Step 1: Navigate to Backend Folder

```bash
cd backend
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Success**: Your terminal should show `(venv)` at the beginning.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Wait**: This will download ~200MB of packages. May take 2-5 minutes.

### Step 4: Start the Backend Server

```bash
python run.py
```

**Expected Output**:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

**✅ Backend is now running!** Keep this terminal open.

### Step 5: Open a NEW Terminal for Frontend

In a **NEW terminal window** (don't close the first one):

```bash
cd frontend
python -m http.server 8000
```

**Expected Output**:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**✅ Frontend is now running!** Keep this terminal open.

### Step 6: Open Browser

Go to: **http://localhost:8000**

**✅ Application is now running!**

---

## ✅ TEST THE APPLICATION

### User Features to Test

1. **Home Page** (http://localhost:8000)
   - Click "Submit a Complaint"
   - Fill in the form
   - Click "Submit"
   - You'll get a Complaint ID

2. **Submit Complaint** (http://localhost:8000/submit-complaint.html)
   - Test complaint submission form
   - Enter sample complaint
   - Note the Complaint ID

3. **Track Complaint** (http://localhost:8000/track-complaint.html)
   - Use the ID from step 2
   - Click "Track Complaint"
   - See real-time status

### Admin Features to Test

1. **Admin Login** (http://localhost:8000/admin-login.html)
   - **Email**: `superadmin@grievancehub.com`
   - **Password**: `SuperAdmin@123`
   - Click "Login"

2. **Admin Dashboard** (http://localhost:8000/admin-dashboard.html)
   - See complaint list
   - View analytics
   - Update complaint status
   - See real-time data

---

## 🔐 Demo Credentials

### Super Admin (Full Access)
```
Email: superadmin@grievancehub.com
Password: SuperAdmin@123
```

### Sub Admin (Zone Access)
```
Email: subadmin_zone1@grievancehub.com
Password: SubAdmin@123
```

### Department Admin (Circle Access)
```
Email: deptadmin_circle1@grievancehub.com
Password: DeptAdmin@123
```

---

## 🐛 TROUBLESHOOTING

### Problem 1: "python: command not found"
**Solution**: 
- Python not installed or not in PATH
- [Download Python](https://www.python.org/downloads/)
- Choose "Add Python to PATH" during installation

### Problem 2: "ModuleNotFoundError: No module named 'flask'"
**Solution**:
```bash
# Make sure you're in the backend folder
cd backend
# Make sure virtual environment is activated (see Step 2)
source venv/bin/activate    # macOS/Linux
# OR
venv\Scripts\activate       # Windows
# Then install
pip install -r requirements.txt
```

### Problem 3: "Port 5000 already in use"
**Solution**:
```bash
# Change port in backend/run.py (change line 8)
# OR kill existing process on port 5000
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -i :5000
```

### Problem 4: "Port 8000 already in use"
**Solution**:
```bash
# Use different port
python -m http.server 8001
# Then go to: http://localhost:8001
```

### Problem 5: "http://localhost:8000 shows 404"
**Solution**:
- Make sure you're in the `frontend` folder before running http.server
- Make sure you run: `python -m http.server 8000` (not in backend folder)
- Check that frontend has index.html file

### Problem 6: Backend shows error when submitting complaint
**Solution**:
- Check both terminals are running
- Frontend and Backend must run simultaneously
- Check both have no error messages
- Refresh the browser (Ctrl+R or Cmd+R)

---

## 📞 GET HELP

If you encounter issues:

1. **Check Terminals**: Look for error messages in both terminal windows
2. **Check Browser Console**: Press F12 in browser, go to Console tab
3. **Read Error Messages**: They usually tell you what's wrong
4. **Try Again**: Close everything and start from "HOW TO RUN" section

---

## 📚 NEXT STEPS

After everything is working:

1. **Read Full Documentation**:
   - `README.md` - Project overview
   - `ARCHITECTURE.txt` - System design
   - `FOLDER_STRUCTURE.md` - Complete file guide

2. **Customize**:
   - Edit `frontend/css/style.css` for colors/fonts
   - Edit `frontend/index.html` for content
   - Edit `backend/app/utils.py` for email settings

3. **Deploy**:
   - Read `SETUP.md` for deployment instructions
   - Use Vercel, Heroku, or any hosting service

---

## ✨ WHAT'S INCLUDED

| Component | Count | Details |
|-----------|-------|---------|
| Backend Python Files | 13 | Flask app + routes + models |
| Frontend Files | 11 | 5 HTML + CSS + 5 JS files |
| Documentation | 15+ | Complete setup guides |
| API Endpoints | 19 | Authentication, Complaints, Admin, Zones |
| Database Tables | 9 | Fully normalized schema |
| Total Code | 8000+ | Lines of well-documented code |

---

## 🎉 SUCCESS!

When you see:
- Terminal 1: `Running on http://127.0.0.1:5000` ✅
- Terminal 2: `Serving HTTP on 0.0.0.0 port 8000` ✅
- Browser: Application loads at http://localhost:8000 ✅

**You're all set!**

---

## 📖 DOCUMENTATION FILES

After setup, read these in order:

1. **This File** ← You are here (Master Setup Guide)
2. `START_HERE.md` - Complete overview
3. `QUICKSTART.md` - Quick reference
4. `README.md` - Project details
5. `ARCHITECTURE.txt` - System design
6. `SETUP.md` - Deployment guide
7. `FOLDER_STRUCTURE.md` - File reference
8. `QUICK_REFERENCE.md` - Quick lookup

---

**Happy coding! 🚀**

For questions, check the documentation or review the error messages in your terminal.
