# Grievance Hub - Complete Setup Guide

This guide walks you through setting up and running the complete application locally.

## Prerequisites

- Python 3.8+ installed
- A terminal/command prompt
- (Optional) Google Gemini API key for AI classification
- (Optional) Gmail account for email notifications

## Step 1: Project Structure

The project is organized as:
```
grievanceptoj_realworld/
├── backend/                 # Flask API server
├── frontend/               # Web interface (HTML/CSS/JS)
├── data/                   # Database (created automatically)
└── README.md
```

## Step 2: Backend Setup

### 2.1 Install Python Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2.2 Install Requirements

```bash
pip install -r requirements.txt
```

### 2.3 Configure Environment

Copy the example `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///../data/grievance.db

# Optional: Email notifications
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587

# Optional: AI classification
GEMINI_API_KEY=your_gemini_api_key
```

#### Email Setup (Gmail)

To enable email notifications:

1. Enable 2-Factor Authentication on your Google Account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate an "App Password" for Mail/Windows
4. Copy and paste into `.env` as `EMAIL_PASSWORD`

If you don't configure email:
- OTPs will display in console instead
- Application will still work fully

#### Gemini API Setup (Optional)

For AI-based complaint classification:

1. Get API key from: https://ai.google.dev
2. Add to `.env` as `GEMINI_API_KEY`

If not configured:
- Complaints default to "General" category
- "Non-Critical" severity
- Classification still works

### 2.4 Start the Backend

```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Database will be automatically initialized on first run.

## Step 3: Frontend Setup

### 3.1 Start a Local Server

Keep the backend running in the first terminal, then open a new terminal:

```bash
cd frontend
```

**Option A: Using Python (recommended)**
```bash
python -m http.server 8000
```

**Option B: Using Node.js**
```bash
npx http-server
```

**Option C: Using Live Server** (VS Code extension)
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

### 3.2 Access the Application

Open your browser and navigate to:

- **Home Page**: http://localhost:8000
- **Admin Login**: http://localhost:8000/admin-login.html

## Step 4: Test the Application

### 4.1 User Flow (Public)

1. Go to http://localhost:8000
2. Click "Submit a Complaint"
3. Fill in the form with:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Phone: `9999999999`
   - Zone: Select any zone
   - Locality: Select any area
   - Description: `Road is damaged near my house`
4. Click "Submit Complaint"
5. You'll receive a Complaint ID and OTP (shown on screen)
6. Go to "Track Complaint" to view status

### 4.2 Admin Flow (Protected)

1. Go to http://localhost:8000/admin-login.html
2. Use one of the demo credentials:

**Option 1: Super Admin** (Full Access)
- Email: `superadmin@grievancehub.com`
- Password: `SuperAdmin@123`

**Option 2: Sub Admin** (Zone Access)
- Email: `subadmin_zone1@grievancehub.com`
- Password: `SubAdmin@123`

**Option 3: Department Admin** (Circle Access)
- Email: `deptadmin_circle1@grievancehub.com`
- Password: `DeptAdmin@123`

3. After login, you'll see the admin dashboard with:
   - Statistics (Total, Pending, In Progress, Resolved)
   - Category breakdown
   - All complaints list
   - Filter and search options
   - Update complaint status

## Step 5: Database

### View Database

The SQLite database is stored in `data/grievance.db`

To view it with a GUI tool:
- Download SQLite Browser: https://sqlitebrowser.org/
- Open `data/grievance.db`

### Reset Database

To reset and start fresh:

```bash
cd backend
rm data/grievance.db
python run.py
```

This will recreate the database with fresh seed data.

## Common Issues & Fixes

### Issue: "Address already in use" for port 5000

**Solution:** Use a different port
```bash
FLASK_PORT=5001 python run.py
```

Then update `frontend/js/config.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001';
```

### Issue: CORS error - "No 'Access-Control-Allow-Origin' header"

**Solution:** Ensure Flask CORS is initialized (it is by default in `app/__init__.py`)

Also verify `API_BASE_URL` in `frontend/js/config.js` matches your backend URL.

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:** Make sure you're in the `backend` directory when running Python:
```bash
cd backend
python run.py
```

### Issue: Email not sending

**Checklist:**
- [ ] `.env` has EMAIL_USER and EMAIL_PASSWORD
- [ ] Using App Password (not regular Google password)
- [ ] 2FA enabled on Google Account
- [ ] Internet connection active
- [ ] Check console for error messages

### Issue: "No such table" error

**Solution:** Database not initialized
```bash
cd backend
python -c "from app import create_app, db; app = create_app(); db.create_all()"
```

## API Testing

Use curl or Postman to test endpoints:

### Submit Complaint
```bash
curl -X POST http://localhost:5000/api/complaints/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9999999999",
    "description": "Road is damaged",
    "area_id": 1
  }'
```

### Track Complaint
```bash
curl -X POST http://localhost:5000/api/complaints/track \
  -H "Content-Type: application/json" \
  -d '{
    "complaint_id": "CMP12345678",
    "email": "john@example.com",
    "otp": "123456"
  }'
```

### Admin Login
```bash
curl -X POST http://localhost:5000/api/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "superadmin@grievancehub.com",
    "password": "SuperAdmin@123"
  }'
```

## Production Deployment

For production deployment:

1. **Update `.env`:**
   - Set `FLASK_ENV=production`
   - Use PostgreSQL instead of SQLite
   - Set secure `DATABASE_URL`

2. **Security:**
   - Use HTTPS
   - Set strong admin passwords
   - Implement rate limiting
   - Add request validation

3. **Hosting Options:**
   - Heroku
   - AWS (EC2, Elastic Beanstalk)
   - DigitalOcean
   - Vercel (backend via API)

## Troubleshooting Command Reference

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Reinstall requirements
pip install --upgrade -r requirements.txt

# Run backend in debug mode
FLASK_DEBUG=1 python run.py

# Access database
sqlite3 data/grievance.db

# Kill process on port 5000 (macOS/Linux)
lsof -ti:5000 | xargs kill -9

# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Next Steps

After setup, you can:

1. **Customize Themes:** Edit `frontend/css/style.css`
2. **Add Features:** Extend routes in `backend/app/routes/`
3. **Improve AI:** Add custom Gemini prompts in `backend/app/utils.py`
4. **Add Database:** Migrate from SQLite to PostgreSQL
5. **Deploy:** Push to production hosting

## Support

For issues:
1. Check this guide's "Common Issues" section
2. Check `README.md` for technical details
3. Look at console/terminal output for error messages
4. Inspect browser console (F12) for frontend errors

---

**You're all set! Happy testing!** 🚀
