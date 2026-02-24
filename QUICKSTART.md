# Quick Start - 5 Minutes to Running

Follow these steps to get the application running locally in minutes.

## Prerequisites
- Python 3.8+ installed
- Terminal access

## Step 1: Backend (Terminal 1)

```bash
cd backend
python -m venv venv

# Activate (Windows: venv\Scripts\activate)
source venv/bin/activate

pip install -r requirements.txt

python run.py
```

**Wait for:** `Running on http://127.0.0.1:5000`

## Step 2: Frontend (Terminal 2)

```bash
cd frontend
python -m http.server 8000
```

**Wait for:** `Serving HTTP on port 8000`

## Step 3: Open Browser

Go to: **http://localhost:8000**

## 🎉 You're Running!

### Try These:

**As a User:**
1. Click "Submit a Complaint"
2. Fill form and submit
3. Click "Track Complaint" to see status

**As an Admin:**
1. Click "Admin Login"
2. Enter: `superadmin@grievancehub.com` / `SuperAdmin@123`
3. See dashboard with all complaints

## 📋 Demo Accounts

```
Super Admin:
  Email: superadmin@grievancehub.com
  Pass:  SuperAdmin@123

Sub Admin:
  Email: subadmin_zone1@grievancehub.com
  Pass:  SubAdmin@123

Dept Admin:
  Email: deptadmin_circle1@grievancehub.com
  Pass:  DeptAdmin@123
```

## ⚙️ Configuration (Optional)

For email notifications, create `backend/.env`:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
GEMINI_API_KEY=your_api_key
```

See [SETUP.md](SETUP.md) for detailed configuration.

## ❌ Issues?

- **Port 5000 in use?** Run: `FLASK_PORT=5001 python run.py`
- **Can't connect?** Check firewall, ensure both terminals show "Running"
- **Database error?** Delete `data/grievance.db` and restart

See [SETUP.md](SETUP.md) for troubleshooting guide.

---

**Need more details?** → Read [README.md](README.md) and [SETUP.md](SETUP.md)

**API Documentation?** → Check [README.md](README.md#-api-endpoints)
