# Quick Start Guide - Modular Grievance System

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment (2 min)
```bash
cd scripts/

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# EMAIL_USER=your-email@gmail.com
# GEMINI_API_KEY=your-api-key
```

### Step 2: Install Dependencies (2 min)
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database (1 min)
```bash
python init_db.py
python seed_db.py
```

### Step 4: Run the App
```bash
python run.py
```

✅ **App is running at http://localhost:5000**

---

## 📁 Folder Structure at a Glance

```
scripts/
├── app/                    ← Main application
│   ├── models/            ← Database operations
│   ├── routes/            ← API endpoints
│   ├── services/          ← Business logic
│   └── utils/             ← Helper functions
├── run.py                 ← Start here
├── init_db.py            ← Initialize database
├── seed_db.py            ← Seed test data
└── requirements.txt      ← Dependencies
```

---

## 🔌 API Endpoints

### User API
```
POST /api/auth/send-otp              # Get OTP
POST /api/auth/verify-otp            # Verify OTP
POST /api/complaints/submit          # Submit complaint
POST /api/complaints/track           # Track complaint
GET  /api/zones                      # Get zones
GET  /api/areas                      # Get areas
GET  /api/categories                 # Get categories
```

### Admin API
```
POST /api/admin/login                # Login as admin
GET  /api/admin/complaints           # Get complaints
PUT  /api/admin/complaints/<id>/status  # Update status
GET  /api/admin/profile              # Get profile
POST /api/admin/logout               # Logout
```

---

## 📝 Configuration

### Email Setup (Gmail)
1. Enable 2FA on Gmail account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Add to `.env`:
```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Gemini API Setup
1. Get API key: https://aistudio.google.com/
2. Add to `.env`:
```env
GEMINI_API_KEY=your-api-key
```

---

## 👤 Test Logins

After running `seed_db.py`, use these credentials:

**Super Admin**
- Email: `superadmin@grievancehub.com`
- Password: `superadmin@123`

**Zone Admin (Zone 1)**
- Email: `zone1admin@grievancehub.com`
- Password: `zone1admin@123`

**Department Admin**
- Email: `dept1@grievancehub.com`
- Password: `dept1admin@123`

---

## 🆘 Troubleshooting

### Module not found error
```bash
# Make sure you're in the scripts directory
cd scripts/
python run.py
```

### Database not found
```bash
# Initialize the database
python init_db.py
python seed_db.py
```

### Email not sending
- Check `.env` has correct credentials
- Check 2FA and App Password for Gmail
- Check EMAIL_PORT is 587

### Gemini API not working
- Verify GEMINI_API_KEY in `.env`
- Check API is enabled in Google Cloud

---

## 📚 Full Documentation

For complete documentation, see:
- `MODULAR_STRUCTURE_GUIDE.md` - Complete guide with architecture
- `FILE_STRUCTURE_SUMMARY.md` - File-by-file breakdown

---

## 🎯 Key Files to Know

- `run.py` - Start the application
- `app/config.py` - All configuration
- `app/routes/` - All API endpoints
- `app/models/` - Database operations
- `app/services/` - Business logic
- `.env` - Your secrets (don't commit!)

---

## ✅ Verify Installation

```bash
# Test the app is working
curl http://localhost:5000/

# Should return:
# {
#   "message": "Grievance System API - Multi-Admin Version",
#   "status": "running",
#   ...
# }
```

---

## 📦 What Changed?

**Nothing in functionality!**
- ✅ Same API endpoints
- ✅ Same database schema
- ✅ Same business logic
- ✅ Same performance
- ✅ Only better organization

**Benefits:**
- Easier to maintain
- Easier to test
- Easier to add features
- Easier to debug
- Professional structure

---

## 🚀 Deploy to Production

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables on production
export GEMINI_API_KEY=...
export EMAIL_USER=...
export EMAIL_PASSWORD=...

# Run with production server (not flask debug)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app.main:app'
```

---

## 📞 Need Help?

1. Check the specific module's file
2. Read the comprehensive guide: `MODULAR_STRUCTURE_GUIDE.md`
3. Review `.env.example` for all config options
4. Check the models/ folder for database operations
5. Check the routes/ folder for API logic

---

**Everything works exactly like before, just better organized!** 🎉
