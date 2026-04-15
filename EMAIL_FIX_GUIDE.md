# Email Configuration Fix Guide

## The Problem

You're getting this error when trying to send OTP emails:
```
(535, b'5.7.8 Username and Password not accepted...')
```

**Why?** Gmail doesn't allow apps to use your regular Gmail password. It's a security feature.

---

## The Solution (3 minutes)

### Step 1: Enable 2-Factor Authentication (if not already enabled)

1. Go to: https://myaccount.google.com/security
2. Look for "2-Step Verification"
3. If it says "Off", click it and enable it
4. Follow Google's steps (you'll get codes on your phone)

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. You should see a dropdown that says "Select the app and device you're using"
3. Select: **Mail** from the first dropdown
4. Select: **Windows Computer** (or your device type) from the second dropdown
5. Click **Generate**
6. Google will show you a 16-character password like: `xxxx xxxx xxxx xxxx`
7. **Copy this password** (including the spaces)

### Step 3: Update Your `.env` File

Open `/scripts/.env` and update these lines:

```
EMAIL_USER=your-actual-email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_FROM=your-actual-email@gmail.com
```

**Important:** 
- Use the App Password you just generated, NOT your regular Gmail password
- Keep the spaces in the password - don't remove them
- Don't share this password

### Step 4: Restart Your App

```bash
python run.py
```

Now try sending an OTP - it should work!

---

## Testing the Email

Try this in Python to test:

```python
from app.services.email_service import send_email

success = send_email(
    'test@example.com',
    'Test Email',
    'This is a test email'
)

print(f"Email sent: {success}")
```

---

## What Changed in the Code?

I improved the `email_service.py` file to:

1. **Strip whitespace** from password (common issue with `.env` files)
2. **Add timeout** to prevent hanging (10 seconds)
3. **Better error messages** showing exactly what's wrong
4. **Catch authentication errors** specifically to give you helpful info

These improvements will help debug email issues faster in the future.

---

## Common Issues & Fixes

### Issue 1: "App Password" option doesn't appear
**Fix:** You need to enable 2-Factor Authentication first (Step 1 above)

### Issue 2: Error says "Less secure apps"
**Fix:** You're using your regular password instead of App Password. Use the 16-character password from Step 2.

### Issue 3: Password has special characters and doesn't work
**Fix:** Try removing special characters or use quotes around it in `.env`:
```
EMAIL_PASSWORD="xxxx xxxx xxxx xxxx"
```

### Issue 4: It still doesn't work
**Fix:** Try using a different email provider:
- **SendGrid**: More reliable for production
- **Mailgun**: Better for high volume
- **AWS SES**: If using AWS already

---

## Email Configuration for Other Providers

### SendGrid (Alternative)

```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USER=apikey
EMAIL_PASSWORD=SG.your-sendgrid-api-key
EMAIL_FROM=your-email@example.com
```

### Mailgun (Alternative)

```
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USER=postmaster@your-domain.mailgun.org
EMAIL_PASSWORD=your-mailgun-password
EMAIL_FROM=your-email@example.com
```

---

## Quick Checklist

- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App Password generated from Google Account
- [ ] `.env` file updated with App Password
- [ ] No typos in EMAIL_USER or EMAIL_PASSWORD
- [ ] Password includes spaces (xxxx xxxx xxxx xxxx)
- [ ] App restarted after .env change
- [ ] Test OTP email sent successfully

---

## Still Not Working?

Run this to debug:

```bash
python -c "from app.config import log_email_config; log_email_config()"
```

You'll see what's configured. If EMAIL_PASSWORD shows as empty, your `.env` file isn't being read.

Check that `.env` file exists in `/scripts/` folder (not in a different folder).
