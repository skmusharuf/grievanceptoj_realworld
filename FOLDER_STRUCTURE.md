# Complete Folder Structure Guide

## Project Overview

Your Grievance Hub application has been restructured into a clean, modular architecture with separate backend and frontend folders.

---

## Complete Folder Tree

```
grievanceptoj_realworld/
│
├── backend/                              # Flask Application Backend
│   ├── app/                              # Main Flask Application Package
│   │   ├── __init__.py                  # Flask app factory & initialization
│   │   ├── models.py                    # SQLAlchemy ORM models (all database tables)
│   │   ├── utils.py                     # Utility functions (OTP, Email, AI classification)
│   │   └── routes/                      # API Route Blueprints
│   │       ├── __init__.py              # Routes package initialization
│   │       ├── auth_routes.py           # Authentication endpoints (login, OTP, sessions)
│   │       ├── complaint_routes.py      # Complaint CRUD endpoints
│   │       ├── admin_routes.py          # Admin dashboard & analytics endpoints
│   │       └── zone_routes.py           # Zone/Area/Circle data endpoints
│   ├── scripts/                          # Utility Scripts
│   │   ├── __init__.py                  # Scripts package initialization
│   │   └── seed_db.py                   # Database seeding script (demo data)
│   ├── run.py                           # Main Flask application entry point
│   ├── requirements.txt                 # Python dependencies for backend
│   └── .env.example                     # Environment variables template
│
├── frontend/                             # Vanilla HTML/CSS/JavaScript Frontend
│   ├── index.html                       # Home/Landing Page
│   ├── submit-complaint.html            # Complaint Submission Form Page
│   ├── track-complaint.html             # Complaint Tracking Page
│   ├── admin-login.html                 # Admin Login Page
│   ├── admin-dashboard.html             # Admin Dashboard Page
│   ├── css/                             # Stylesheets
│   │   └── style.css                    # Main CSS file (all page styles)
│   └── js/                              # JavaScript Modules
│       ├── config.js                    # API configuration & constants
│       ├── submit-complaint.js          # Submit complaint page logic
│       ├── track-complaint.js           # Track complaint page logic
│       ├── admin-login.js               # Admin login logic
│       └── admin-dashboard.js           # Admin dashboard logic
│
├── data/                                 # Data Files (created at runtime)
│   ├── grievance.db                     # SQLite Database (created when running backend)
│   ├── complaints.json                  # Sample complaint data
│   └── otp_storage.json                 # OTP storage
│
├── models/                               # Machine Learning Models
│   ├── category_model.pkl               # Complaint category classification model
│   ├── criticality_model.pkl            # Complaint criticality classification model
│   ├── category_vectorizer.pkl          # TF-IDF vectorizer for categories
│   ├── criticality_vectorizer.pkl       # TF-IDF vectorizer for criticality
│   ├── hybrid_lr.pkl                    # Hybrid classification model
│   ├── label_encoder.pkl                # Label encoder
│   ├── tfidf_vectorizer.pkl             # TF-IDF vectorizer
│   ├── critical_keywords.pkl            # Critical keywords dictionary
│   └── base_nb.pkl                      # Naive Bayes base model
│
├── public/                               # Static Assets (for frontend)
│   ├── placeholder-logo.png             # Logo image
│   ├── placeholder-logo.svg             # Logo SVG
│   ├── placeholder-user.jpg             # User placeholder image
│   ├── placeholder.jpg                  # General placeholder image
│   └── placeholder.svg                  # General placeholder SVG
│
├── Documentation Files
│   ├── README.md                        # Project overview & features
│   ├── SETUP.md                         # Detailed setup instructions
│   ├── QUICKSTART.md                    # 5-minute quick start guide
│   ├── RESTRUCTURING_SUMMARY.md         # Architecture & restructuring details
│   ├── FILE_MANIFEST.md                 # Complete file listing & descriptions
│   ├── MIGRATION_CHECKLIST.md           # Verification checklist (100+ items)
│   └── FOLDER_STRUCTURE.md              # This file - folder structure guide
│
├── Configuration Files
│   ├── package.json                     # Node.js dependencies (legacy Next.js setup)
│   ├── package-lock.json                # Locked npm versions
│   ├── pnpm-lock.yaml                   # Locked pnpm versions
│   ├── next.config.mjs                  # Next.js configuration (legacy)
│   ├── tsconfig.json                    # TypeScript configuration (legacy)
│   ├── postcss.config.mjs               # PostCSS configuration (legacy)
│   └── components.json                  # shadcn/ui configuration (legacy)
│
├── Legacy Files
│   ├── app/                             # Old Next.js Application (being replaced)
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── loading.tsx
│   │   ├── admin/
│   │   ├── submit-complaint/
│   │   └── track/
│   │
│   ├── components/                      # Old React Components (being replaced)
│   │   ├── ui/                         # shadcn UI components
│   │   ├── admin-analytics.tsx
│   │   ├── complaint-form.tsx
│   │   └── theme-provider.tsx
│   │
│   ├── hooks/                           # Old React Hooks (being replaced)
│   │   ├── use-mobile.ts
│   │   └── use-toast.ts
│   │
│   ├── lib/                             # Old Utilities (being replaced)
│   │   └── utils.ts
│   │
│   ├── styles/                          # Old CSS (being replaced)
│   │   └── globals.css
│   │
│   └── requirements.txt                 # Old Python requirements
│
└── scripts/                              # Old Scripts (original implementation)
    ├── app2createdinfeb.py              # Original monolithic Flask app
    ├── init_db.py                       # Old database initialization
    ├── seed_db.py                       # Old database seeding
    ├── train_models.py                  # ML model training
    ├── testpred.py                      # Model testing
    └── models/                          # Pickled ML models
```

---

## Key Directories Explained

### Backend Directory (`/backend`)

**Purpose:** Flask REST API server handling all business logic

**Core Components:**
- `app/__init__.py` - Flask app factory that creates and configures the Flask application
- `app/models.py` - SQLAlchemy ORM models defining database schema
- `app/utils.py` - Helper functions for email, OTP, and AI classification
- `app/routes/*.py` - REST API endpoint blueprints

**How It Works:**
1. `run.py` starts the Flask server
2. Routes in `/routes/` handle incoming HTTP requests
3. Models in `models.py` interact with the SQLite database
4. Utils provide shared functionality

### Frontend Directory (`/frontend`)

**Purpose:** Vanilla HTML/CSS/JavaScript user interface

**Pages:**
- `index.html` - Home page
- `submit-complaint.html` - Users submit complaints
- `track-complaint.html` - Users track complaint status
- `admin-login.html` - Admin authentication
- `admin-dashboard.html` - Admin panel with analytics

**Styling & Logic:**
- `css/style.css` - All CSS for all pages (responsive design)
- `js/config.js` - API endpoints and constants
- `js/*.js` - Page-specific JavaScript logic

### Data Directory (`/data`)

**Purpose:** Runtime data storage

**Contents:**
- `grievance.db` - SQLite database (created after first run)
- `complaints.json` - Sample data
- `otp_storage.json` - OTP verification codes

### Models Directory (`/models`)

**Purpose:** Pre-trained Machine Learning models

**Files:**
- `category_model.pkl` - Classifies complaint category
- `criticality_model.pkl` - Classifies complaint severity
- Vectorizers and encoders for ML processing

---

## File Descriptions by Category

### Backend Application Files (Python)

| File | Purpose | Key Functions |
|------|---------|----------------|
| `backend/app/__init__.py` | App factory | Creates Flask app, initializes database, registers blueprints |
| `backend/app/models.py` | ORM Models | Define User, Admin, Complaint, Zone, Area, Circle, AdminSession tables |
| `backend/app/utils.py` | Utilities | OTP generation, email sending, AI classification, phone validation |
| `backend/app/routes/auth_routes.py` | Auth API | POST `/api/auth/login`, `/api/auth/verify-otp`, `/api/auth/logout` |
| `backend/app/routes/complaint_routes.py` | Complaint API | POST/GET `/api/complaints`, `/api/complaints/<id>/status`, `/api/complaints/<id>` |
| `backend/app/routes/admin_routes.py` | Admin API | GET `/api/admin/dashboard`, `/api/admin/analytics`, `/api/admin/complaints` |
| `backend/app/routes/zone_routes.py` | Zone API | GET `/api/zones`, `/api/zones/<id>/circles`, `/api/circles/<id>/areas` |
| `backend/run.py` | Entry Point | Starts Flask development server on port 5000 |
| `backend/scripts/seed_db.py` | Database Seeding | Populates database with demo zones, circles, areas, admins, complaints |

### Frontend Files (HTML/CSS/JavaScript)

| File | Purpose |
|------|---------|
| `frontend/index.html` | Landing page with navigation and call-to-action buttons |
| `frontend/submit-complaint.html` | Form to submit new complaints with categories, description, location |
| `frontend/track-complaint.html` | Search and display complaint status using complaint ID and phone number |
| `frontend/admin-login.html` | Admin authentication form |
| `frontend/admin-dashboard.html` | Admin dashboard with statistics, complaint list, filters |
| `frontend/css/style.css` | All styling for all pages (1000+ lines, fully responsive) |
| `frontend/js/config.js` | API base URL and helper fetch functions |
| `frontend/js/submit-complaint.js` | Form validation, API calls, confirmation handling |
| `frontend/js/track-complaint.js` | Search logic, status display, real-time updates |
| `frontend/js/admin-login.js` | Authentication, session management, redirects |
| `frontend/js/admin-dashboard.js` | Dashboard rendering, charts, complaint filtering, status updates |

---

## Steps to Run the Application

### Prerequisites
- Python 3.8+ installed
- Node.js (optional, only for frontend testing)
- Git

### Step 1: Clone/Navigate to Project
```bash
cd grievanceptoj_realworld
```

### Step 2: Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional, uses defaults if not present)
cp .env.example .env

# Initialize database (creates grievance.db with schema)
python scripts/seed_db.py

# Start Flask server
python run.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
```

The backend is now running at `http://localhost:5000`

### Step 3: Start the Frontend Server

**Option A: Using Python (Recommended)**
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start simple HTTP server
python -m http.server 8000
```

**Option B: Using Node.js**
```bash
# Install a simple server (if not already installed)
npm install -g http-server

# Start server in frontend directory
http-server . -p 8000
```

**Expected Output:**
```
Starting up http-server, serving .
Hit CTRL-C to stop the server
```

### Step 4: Access the Application

Open your browser and navigate to:

- **Home Page:** http://localhost:8000
- **Submit Complaint:** http://localhost:8000/submit-complaint.html
- **Track Complaint:** http://localhost:8000/track-complaint.html
- **Admin Login:** http://localhost:8000/admin-login.html
- **Admin Dashboard:** http://localhost:8000/admin-dashboard.html (after login)

---

## Test Credentials (After Running Seed Script)

### Super Admin Account
- **Email:** `superadmin@grievancehub.com`
- **Password:** `SuperAdmin@123`
- **Access:** Full system access

### Sub Admin Account
- **Email:** `subadmin_zone1@grievancehub.com`
- **Password:** `SubAdmin@123`
- **Access:** Zone 1 management

### Department Admin Account
- **Email:** `deptadmin_circle1@grievancehub.com`
- **Password:** `DeptAdmin@123`
- **Access:** Circle 1 management

---

## API Endpoints Overview

### Authentication Endpoints
```
POST   /api/auth/login              - Admin login with email
POST   /api/auth/verify-otp         - Verify OTP sent to email
POST   /api/auth/logout             - Logout admin
GET    /api/auth/user               - Get current admin user
```

### Complaint Endpoints
```
POST   /api/complaints              - Submit new complaint
GET    /api/complaints              - List all complaints (with filters)
GET    /api/complaints/<id>         - Get specific complaint details
GET    /api/complaints/<id>/status  - Get complaint status for user
PUT    /api/complaints/<id>/status  - Update complaint status (admin)
DELETE /api/complaints/<id>         - Delete complaint (admin)
```

### Admin Dashboard Endpoints
```
GET    /api/admin/dashboard         - Dashboard statistics
GET    /api/admin/analytics         - Analytics data (charts)
GET    /api/admin/complaints        - Paginated complaint list
```

### Zone/Area Endpoints
```
GET    /api/zones                   - Get all zones
GET    /api/zones/<id>/circles      - Get circles in a zone
GET    /api/circles/<id>/areas      - Get areas in a circle
```

---

## Important Notes

1. **Database:** SQLite database (`grievance.db`) is created automatically in the `data/` folder when you run the backend
2. **Environment Variables:** Optional `.env` file in `backend/` folder for configuration
3. **ML Models:** Pre-trained models in `/models/` folder are used for complaint classification
4. **CORS:** Frontend can call backend API without issues (configured in Flask app)
5. **Static Files:** Frontend files are completely independent and don't require build process

---

## Troubleshooting

### Backend won't start
```bash
# Make sure Python virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend can't connect to backend
- Ensure backend is running on `http://localhost:5000`
- Check firewall settings
- Frontend automatically redirects to `http://localhost:8000/admin-login.html` on login

### Database errors
- Delete `data/grievance.db` file
- Run `python scripts/seed_db.py` again
- This will recreate fresh database with demo data

### Port already in use
- Backend: Change port in `backend/run.py` (default 5000)
- Frontend: Use different port `python -m http.server 9000`
- Update `frontend/js/config.js` with new backend URL

---

## Quick Reference

| Task | Command |
|------|---------|
| Start Backend | `cd backend && source venv/bin/activate && python run.py` |
| Start Frontend | `cd frontend && python -m http.server 8000` |
| Seed Database | `cd backend && python scripts/seed_db.py` |
| Access Home | `http://localhost:8000` |
| Access Admin | `http://localhost:8000/admin-login.html` |
| Backend API | `http://localhost:5000/api/...` |
| View Database | Use any SQLite viewer on `data/grievance.db` |

