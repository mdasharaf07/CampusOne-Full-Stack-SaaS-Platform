## 🚀 Step 1: Environment Setup & Installation
First, ensure you have a virtual environment created and all necessary dependencies installed.

### 🍎 For macOS / Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 🪟 For Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🛠️ Step 2: Automated Security Key Generation
Once your environment is ready, run our utility to generate high-entropy security keys.
**This script automatically handles:**
- `JWT_SECRET`: For secure user session tokens.
- `CRYPTO_KEY`: For symmetric AES-256 encryption of sensitive data.
- `RSA_PRIVATE_KEY` & `RSA_PUBLIC_KEY`: For asymmetric signing protocols.

---
## 📧 Step 3: Email Configuration (Gmail SMTP)
The system sends OTPs and notifications via Gmail.

1. **MAIL_USERNAME**: Your Gmail address (e.g., `example@gmail.com`).
2. **MAIL_PASSWORD**: You must use a **Google App Password**.
   - Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
   - Select "Mail" and "Other (Custom Name)".
   - Copy the **16-character code** (e.g., `qzwd nqle woqu llsw`) and paste it here.

---

## ☁️ Step 4: Google Cloud & Sheets Integration
This integration is essential for generating automated certificates (stored in Google Drive) and syncing event data to a Master Spreadsheet.

### A. Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on **Select a project** > **New Project**.
3. Give it a name like `CampusHub-System` and click **Create**.

### B. Enable Required APIs
You must enable the following APIs for your project:
1. Search for **"Google Drive API"** and click **Enable**.
2. Search for **"Google Sheets API"** and click **Enable**.

### C. Create a Service Account & JSON Key
1. In the sidebar, go to **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **Service Account**.
3. Enter a name (e.g., `campushub-bot`) and click **Create and Continue**.
4. Grant the role **Editor** (or owner) and click **Done**.
5. Click on the newly created Service Account in the list.
6. Go to the **Keys** tab > **Add Key** > **Create New Key**.
7. Select **JSON** and click **Create**. A file will download to your computer.
8. **Action**: Open this file, copy its **entire content**, and paste it into `.env` as `GOOGLE_CREDENTIALS_JSON`.

### D. Setup the Master Spreadsheet
1. Create a new Google Sheet at [sheets.new](https://sheets.new).
2. Copy the URL from your browser's address bar.
3. **Action**: Paste the URL into `.env` as `DEFAULT_MASTER_GSHEET_LINK`.
4. **Action**: Click **Share** on the top right of the Google Sheet.
5. **Critical**: Invite the `client_email` address (found inside your `GOOGLE_CREDENTIALS_JSON`) as an **Editor**.

---

## 🗄️ Step 5: Database Connection & Initialization
The system is optimized for PostgreSQL (Neon.tech).

1. **DATABASE_URL**: 
   - Create a free PostgreSQL instance on [Neon.tech](https://neon.tech/).
   - Copy the **Connection String** (e.g., `postgresql://neondb_owner:pass@host/neondb?sslmode=require`).
   - Paste it into your `.env`.

2. **Initialize Tables**:
   Run the following command to create all tables, triggers, and prepopulate the system data:
   ```bash
   python3 backend/database_creation.py
   ```
   *This script uses the centralized `backend/database_full_schema.sql` to ensure your local or cloud database is perfectly synchronized.*

---

## 💳 Step 6: Payment Gateway (Razorpay)
To enable paid event registrations:

1. **RAZORPAY_KEY_ID**: Found in your Razorpay Dashboard -> Settings -> API Keys.
2. **RAZORPAY_KEY_SECRET**: Generated alongside your Key ID.

---

## ⚠️ Security Best Practices
> [!CAUTION]
> **NEVER** commit your `.env` file to GitHub or any public repository. 
> The `.env` file contains absolute power over your database, emails, and payments. Always ensure it is listed in your `.gitignore` file.

---

## 📜 Full .env Template
If you are starting from zero, copy this template:

```env
# Security (Generated via script)
JWT_SECRET=''
CRYPTO_KEY=''
RSA_PRIVATE_KEY=''
RSA_PUBLIC_KEY=''

# Email
MAIL_USERNAME=""
MAIL_PASSWORD=""

# Database
DATABASE_URL=""

# Google Integrations
GOOGLE_CREDENTIALS_JSON=''
DEFAULT_MASTER_GSHEET_LINK=""

# Payments
RAZORPAY_KEY_ID=""
RAZORPAY_KEY_SECRET=""
```
