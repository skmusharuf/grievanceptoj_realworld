# How to Run the Grievance Hub Application

This is a **two-part application**:
- **Backend**: Flask with SQLAlchemy ORM (port 5000)
- **Frontend**: Next.js React (port 3000)

---

## Step 1: Setup Backend

### Open Terminal 1:

```bash
cd backend
```

### Create Virtual Environment:

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

### Initialize Database:

```bash
python scripts/seed_db.py
```

### Run Backend:

```bash
python run.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
```

---

## Step 2: Setup Frontend

### Open Terminal 2 (in the project root):

```bash
npm install
npm run dev
```

**Expected output:**
```
  ▲ Next.js 15.x ready in 1.5s
  ➜ Local: http://localhost:3000
```

---

## Step 3: Access the Application

Open your browser and go to: **http://localhost:3000**

---

## Demo Accounts:

### Super Admin (All Zones):
- **Email**: `superadmin@grievancehub.com`
- **Password**: `SuperAdmin@123`

### Zone Admin (Zone 1):
- **Email**: `zone1admin@grievancehub.com`
- **Password**: `zone1admin@123`

### Department Admin:
- **Email**: `deptadmin_circle1@grievancehub.com`
- **Password**: `DeptAdmin@123`

---

## Features to Test:

1. **Home Page** - View landing page
2. **Submit Complaint** - 4-step form with voice input and pie charts
3. **Track Complaint** - Track using Complaint ID and OTP
4. **Admin Dashboard** - View analytics and manage complaints

---

## Troubleshooting:

**Backend won't start?**
- Make sure you're in the `backend/` folder
- Check if port 5000 is available
- Verify all dependencies installed: `pip list | grep flask`

**Frontend won't start?**
- Make sure you're in the project root
- Run `npm install` again
- Check if port 3000 is available

**API Connection Error?**
- Make sure backend is running (Terminal 1)
- Check `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:5000`

---

## Environment Variables (.env):

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**Backend (backend/.env):**
```
FLASK_ENV=development
DATABASE_URL=sqlite:///instance/grievance.db
```

---

**That's it! You should have a working application now.** 🎉
