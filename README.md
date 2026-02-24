# Grievance Hub - Citizen Complaint Management System

A modern, full-stack web application for managing citizen grievances and complaints. Built with Flask (SQLAlchemy ORM) backend and vanilla HTML/CSS/JavaScript frontend.

## 🏗️ Project Structure

```
grievanceptoj_realworld/
├── backend/                    # Flask backend with SQLAlchemy
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── models.py          # SQLAlchemy ORM models
│   │   ├── utils.py           # Utility functions (email, classification, OTP)
│   │   └── routes/
│   │       ├── auth_routes.py       # Authentication and login
│   │       ├── complaint_routes.py  # Complaint submission and tracking
│   │       ├── admin_routes.py      # Admin dashboard functionality
│   │       └── zone_routes.py       # Zone and area data endpoints
│   ├── scripts/
│   │   └── seed_db.py         # Database seeding script
│   ├── run.py                 # Application entry point
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
│
├── frontend/                   # Vanilla HTML/CSS/JavaScript
│   ├── index.html             # Home page
│   ├── submit-complaint.html  # Complaint submission form
│   ├── track-complaint.html   # Complaint tracking page
│   ├── admin-login.html       # Admin login page
│   ├── admin-dashboard.html   # Admin dashboard
│   ├── css/
│   │   └── style.css          # All styling (responsive design)
│   └── js/
│       ├── config.js          # API configuration and utilities
│       ├── submit-complaint.js
│       ├── track-complaint.js
│       ├── admin-login.js
│       └── admin-dashboard.js
│
└── data/                       # Database storage (created at runtime)
    └── grievance.db           # SQLite database
```

## 🚀 Quick Start

### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (optional - defaults work for local development)
   ```

4. **Run the server:**
   ```bash
   python run.py
   ```
   Server will start at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd ../frontend
   ```

2. **Start a local server** (recommended - not just opening HTML files):
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js (if available)
   npx http-server
   ```

3. **Open in browser:**
   - Home: `http://localhost:8000`
   - Admin: `http://localhost:8000/admin-login.html`

## 📋 Features

### User Features
- **Submit Complaints:** Detailed form with automatic AI-based classification
- **Track Complaints:** Real-time tracking with status history
- **Email Notifications:** Automatic updates when complaint status changes
- **Multi-language Support:** Auto-translation of complaints to English (Hindi/Telugu)
- **Zone/Area Selection:** Intelligent location mapping to correct departments

### Admin Features
- **Role-based Access:**
  - Super Admin: Full system access
  - Sub Admin: Zone-level management
  - Department Admin: Circle-level management
- **Complaint Management:** View, filter, search, and update complaints
- **Dashboard Analytics:** Stats, category breakdown, and recent complaints
- **Status Management:** Track complaint lifecycle from Pending → In Progress → Resolved
- **Email Notifications:** Automatic customer updates

### System Features
- **AI Classification:** Automatic categorization using Google Gemini
- **OTP Verification:** Secure complaint tracking
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Database:** SQLite with SQLAlchemy ORM
- **Email Integration:** SMTP-based notifications

## 🔐 Authentication

### Demo Credentials

**Super Admin:**
- Email: `superadmin@grievancehub.com`
- Password: `SuperAdmin@123`

**Sub Admin (Zone 1):**
- Email: `subadmin_zone1@grievancehub.com`
- Password: `SubAdmin@123`

**Department Admin:**
- Email: `deptadmin_circle1@grievancehub.com`
- Password: `DeptAdmin@123`

## 📊 Database Schema

### Core Tables
- **zones**: 12 administrative zones
- **circles**: 60 subdivisions (5 per zone)
- **areas**: 300 localities/wards (5 per circle)
- **admins**: Admin users with role-based access
- **complaints**: Grievance records
- **complaint_status_history**: Status change tracking
- **otp_storage**: OTP management for auth and tracking
- **admin_sessions**: Active admin sessions
- **email_notifications**: Email log

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/send-otp` - Send OTP for verification
- `POST /api/auth/verify-otp` - Verify OTP
- `POST /api/auth/admin/login` - Admin login

### Complaints
- `POST /api/complaints/submit` - Submit new complaint
- `POST /api/complaints/track` - Track complaint status
- `POST /api/complaints/classify` - AI classification
- `GET /api/complaints/categories` - Get categories

### Admin
- `GET /api/admin/complaints` - List complaints (filtered by role)
- `PUT /api/admin/complaints/<id>/status` - Update status
- `PUT /api/admin/complaints/<id>/assign` - Assign complaint
- `GET /api/admin/complaints/<id>` - Complaint details
- `GET /api/admin/dashboard-stats` - Dashboard statistics

### Zones & Areas
- `GET /api/zones` - All zones
- `GET /api/areas` - All areas with search
- `GET /api/areas/<zone_id>` - Areas by zone

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Flask
FLASK_ENV=development
DATABASE_URL=sqlite:///../data/grievance.db

# Email (Gmail SMTP)
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587

# Gemini API for classification
GEMINI_API_KEY=your_api_key
```

### Email Setup (Gmail)

1. Enable 2FA on Google Account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in `EMAIL_PASSWORD`

## 🏃 Running the Application

### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
python run.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
python -m http.server 8000
```

Then visit: `http://localhost:8000`

## 📱 Responsive Design

- **Desktop**: Full-width layouts with multi-column grids
- **Tablet**: Adjusted grid columns and touch-friendly buttons
- **Mobile**: Single-column layout, hamburger menu for nav

## 🛠️ Tech Stack

**Backend:**
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.23
- Google Generative AI (Gemini)
- googletrans (for translation)

**Frontend:**
- HTML5
- CSS3 (with CSS Grid & Flexbox)
- Vanilla JavaScript (ES6+)
- No external frameworks

**Database:**
- SQLite

## 📝 Database Initialization

The database is automatically created on first run. To manually initialize:

```bash
cd backend
python run.py
```

This will:
1. Create `data/grievance.db`
2. Create all tables
3. Seed zones, circles, areas, and admin users

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Backend (change port)
FLASK_PORT=5001 python run.py

# Frontend (change port)
python -m http.server 8001
```

### Email Not Sending
- Check `.env` credentials
- Enable Less Secure App Access (if not using App Password)
- Check firewall/antivirus SMTP blocking

### CORS Issues
- Ensure backend CORS is enabled (it is by default)
- Check API_BASE_URL in `frontend/js/config.js`

### Database Locked
- Close all running instances
- Delete `.db-journal` files if they exist
- Restart backend

## 📄 License

This project is built for Hyderabad Municipal Corporation grievance management system.

## 👥 Contacts

For issues or questions, contact the development team.

---

**Version:** 2.0  
**Last Updated:** 2025  
**Status:** Production Ready
