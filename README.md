# CampusOne

A production-oriented full-stack college event management and automation platform designed to streamline the complete lifecycle of campus events, cultural fests, workshops, and student activities.

CampusOne enables institutions, clubs, and student organizations to manage registrations, payments, attendance, invoicing, notifications, and certificate distribution through a centralized and scalable web platform.

---

## Overview

CampusOne follows a decoupled client-server architecture with a lightweight frontend and a modular Python backend. The platform is built to automate operational workflows involved in college event management while maintaining scalability, security, and clean system organization.

The application integrates multiple third-party services including Razorpay, Google Sheets API, Google Drive API, Gmail SMTP, and PostgreSQL to deliver a real-world SaaS-like experience.

---

## Core Features

### Authentication & Security
- JWT-based authentication and session handling
- Role-Based Access Control (RBAC)
- AES-256 and RSA encryption support
- Secure password reset using Email OTP verification
- Protected dashboard routing and authorization checks

### Event Management
- Create and manage cultural events and workshops
- Student event registration system
- Upcoming events listing and participation tracking
- Admin event monitoring dashboard

### Payment Integration
- Razorpay payment gateway integration
- Dynamic payment verification workflow
- Automated transaction handling

### Invoice & Ticket Generation
- Automated PDF invoice and ticket generation
- Local invoice storage management
- Downloadable payment confirmations

### Cloud Automation
- Google Sheets synchronization using Service Accounts
- Automated certificate generation and distribution
- Google Drive integration for cloud-hosted assets

### Notification System
- Email-based OTP authentication
- Registration confirmation emails
- Event reminder notifications
- Automated communication workflows

---

## Tech Stack

### Frontend
- HTML5
- JavaScript
- Tailwind CSS

### Backend
- Python
- Flask / REST APIs

### Database
- PostgreSQL
- Neon.tech

### Integrations & Services
- Razorpay API
- Google Sheets API
- Google Drive API
- Gmail SMTP

### Security
- JWT Authentication
- AES-256 Encryption
- RSA Encryption

---

## System Architecture

```text
Client (Frontend)
        │
        ▼
REST API Layer
        │
        ▼
Python Backend Services
        │
 ┌──────┼──────────┬───────────┬───────────┐
 ▼      ▼          ▼           ▼           ▼
PostgreSQL   Razorpay   Google APIs   Email Service
```

---

## Project Structure

```text
CampusOne/
│
├── frontend/
│   ├── dashboard/
│   ├── js/
│   ├── index.html
│   ├── sign-in.html
│   ├── sign-up.html
│   └── upcoming-events.html
│
├── backend/
│   ├── routes/
│   ├── utils/
│   ├── invoices/
│   ├── uploads/
│   ├── app.py
│   ├── database_creation.py
│   └── database_full_schema.sql
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation & Setup

### Clone Repository

```bash
git clone https://github.com/mdasharaf07/CampusOne-Full-Stack-SaaS-Platform.git
```

### Navigate to Project

```bash
cd CampusOne-Full-Stack-SaaS-Platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the backend directory.

```env
JWT_SECRET=
CRYPTO_KEY=

MAIL_USERNAME=
MAIL_PASSWORD=

GOOGLE_CREDENTIALS_JSON=
DEFAULT_MASTER_GSHEET_LINK=

DATABASE_URL=

RSA_PRIVATE_KEY=
RSA_PUBLIC_KEY=

RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

---

## Database Setup

Run the schema creation script:

```bash
python backend/database_creation.py
```

Or manually execute:

```bash
backend/database_full_schema.sql
```

inside PostgreSQL.

---

## Running the Application

### Start Backend Server

```bash
python backend/app.py
```

### Launch Frontend

Open:

```text
frontend/index.html
```

using Live Server or any local static server.

---

## API Modules

### Authentication
- Sign In
- Sign Up
- Password Recovery
- OTP Verification

### Event Services
- Event Creation
- Event Registration
- Attendance Management

### Financial Services
- Payment Verification
- Invoice Generation

### Automation Services
- Google Sheets Sync
- Certificate Distribution
- Email Notifications

---

## Security Practices

- Encrypted credential handling
- Token-based authentication
- Route protection middleware
- Secure API communication
- Role-based authorization layers

---

## Future Improvements

- Docker containerization
- CI/CD deployment pipelines
- Redis caching layer
- Real-time notifications
- Admin analytics dashboard
- Mobile application support
- AI-powered recommendation engine

---

## Use Cases

- College cultural fest management
- Workshop registration systems
- Technical symposium operations
- Student club event coordination
- Institutional event automation

---

## Repository Topics

```text
full-stack-project
college-event-management
python-backend
postgresql
tailwindcss
jwt-authentication
razorpay-integration
google-sheets-api
automation-platform
saas-platform
```

---

## License

This project is intended for educational, portfolio, and learning purposes.

---

## Author

[Mohamed Asharaf](https://github.com/mdasharaf07)
