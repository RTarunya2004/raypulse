# RayPulse - AI-Powered Customer Experience Intelligence Platform

![RayPulse Logo](https://via.placeholder.com/800x200/667eea/ffffff?text=RayPulse+-+Turn+Silent+Exits+Into+Growth)

## 🚀 Overview

**RayPulse** is a cloud-based SaaS web platform designed to help businesses, factories, and service providers detect customer dissatisfaction early and convert customer experience insights into business growth.

### The Problem

In 2026, **96% of unhappy customers never complain**—they simply stop using products or services. Traditional feedback methods arrive too late.

### The Solution

RayPulse captures real-time customer feedback through QR codes, analyzes it using AI-based sentiment analysis, and provides actionable insights to prevent customer loss and improve revenue.

---

## ✨ Key Features

### 🎯 Core Functionality

- **Instant Feedback Collection** - QR code-based feedback system (no login required)
- **AI Sentiment Analysis** - Advanced NLP using TextBlob for emotion detection
- **Friction Score Calculation** - Proprietary algorithm to detect customer dissatisfaction (0-100 scale)
- **Real-Time Alerts** - Automated notifications when high friction is detected
- **Multi-Tenant Architecture** - Complete data isolation per business
- **Analytics Dashboard** - Real-time charts and trends powered by Chart.js

### 📊 Business Intelligence

- **Experience Score Tracking** - Monitor customer satisfaction trends over time
- **Risk Classification** - Automatic categorization (HIGH/MEDIUM/LOW risk)
- **Actionable Recommendations** - AI-powered insights for operational improvements
- **Revenue Protection** - Early detection prevents customer loss

### 🔒 Security & Privacy

- **Secure Authentication** - Password hashing with Werkzeug
- **Data Isolation** - Multi-tenant architecture with separate business databases
- **Anonymous Feedback** - No customer login required (privacy-first design)
- **HTTPS Ready** - Production-ready security configuration

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0 (Web Framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- SQLite/MySQL (Database)

**AI/ML:**
- TextBlob (Sentiment Analysis)
- NLTK (Natural Language Processing)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5.3 (UI Framework)
- Chart.js 4.4 (Data Visualization)
- Bootstrap Icons

**Features:**
- QRCode Generation
- Multi-tenant SaaS Model

### Project Structure

```
raypulse/
├── app.py                  # Main Flask application
├── models/
│   └── models.py          # Database models (Business, Feedback, Alert)
├── utils/
│   └── sentiment_analyzer.py  # AI sentiment analysis engine
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   ├── register.html      # Business registration
│   ├── login.html         # Business login
│   ├── feedback.html      # Customer feedback form
│   ├── feedback_success.html  # Thank you page
│   ├── dashboard.html     # Business analytics dashboard
│   └── alerts.html        # Alerts & recommendations
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/               # JavaScript files
│   └── images/           # Images and assets
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download

```bash
cd raypulse
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

The database will be automatically created when you first run the application.

### Step 5: Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

---

## 📖 User Guide

### For Business Owners

#### 1. **Register Your Business**
   - Navigate to http://localhost:5000
   - Click "Get Started" or "Register"
   - Fill in:
     - Business Name
     - Business Type
     - Email
     - Password
   - System automatically generates:
     - Unique Company ID (e.g., RP4A2B3C4D5E6F)
     - Feedback URL
     - QR Code

#### 2. **Access Dashboard**
   - Login with your credentials
   - View real-time metrics:
     - Total Feedback Count
     - Average Rating
     - High Risk Alerts
     - Satisfaction Rate

#### 3. **Deploy QR Code**
   - Download QR code from dashboard
   - Print on:
     - Product packaging
     - Receipts
     - Store displays
     - Service locations

#### 4. **Monitor & Act**
   - Review real-time feedback
   - Check friction alerts
   - Follow AI recommendations
   - Improve operations based on insights

### For Customers

#### 1. **Scan QR Code**
   - Use smartphone camera
   - Scan QR code on product/receipt

#### 2. **Submit Feedback**
   - Rate experience (1-5 stars)
   - Select emotion (😊 😐 😡)
   - Add optional comments
   - Submit (no login required)

#### 3. **Done!**
   - Instant submission
   - Anonymous & secure
   - Helps business improve

---

## 🎯 Real-World Use Case

### Manufacturing Factory Scenario

**Problem:**
- Factory experiencing 18% product return rate
- Customer complaints unclear
- Revenue loss from dissatisfaction

**RayPulse Implementation:**
1. QR code printed on product packaging
2. Customers scan after delivery
3. RayPulse detects:
   - **31% of feedback** mentions delivery delays
   - High friction score in logistics stage
   - Risk alerts triggered

**Results:**
- Transport process improved
- Return rate reduced by **47%**
- Customer satisfaction increased
- Revenue protected through early intervention

---

## 🔧 Configuration

### Database Configuration

By default, RayPulse uses SQLite. To use MySQL:

```python
# In app.py, change:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/raypulse'
```

### Production Deployment

For production, update:

1. **Secret Key** - Use environment variable:
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

2. **Debug Mode** - Disable:
```python
app.run(debug=False)
```

3. **HTTPS** - Enable SSL certificate

4. **Database** - Use production-grade database (PostgreSQL/MySQL)

---

## 📊 AI/ML Components

### Sentiment Analysis Engine

**Algorithm:**
- Uses TextBlob polarity analysis
- Converts -1 to 1 scale → 0 to 1 scale
- Combines with star rating and emotion

**Friction Score Calculation:**
```
Friction Score = (Star Friction × 0.4) + (Emotion Friction × 0.3) + (Sentiment Friction × 0.3)

Where:
- Star Friction = (5 - rating) × 20
- Emotion Friction: Happy=0, Neutral=30, Unhappy=70
- Sentiment Friction = (1 - sentiment_score) × 100
```

**Risk Classification:**
- HIGH: Friction Score ≥ 60
- MEDIUM: Friction Score 30-59
- LOW: Friction Score < 30

---

## 🎨 Customization

### Brand Colors

Edit `static/css/style.css`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    /* Change to your brand colors */
}
```

### Email Notifications

To add email alerts, install:
```bash
pip install Flask-Mail
```

Configure in `app.py`:
```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
```

---

## 🐛 Troubleshooting

### Issue: Database not found
**Solution:** Run `python app.py` to auto-create database

### Issue: NLTK data missing
**Solution:** Run:
```python
import nltk
nltk.download('brown')
nltk.download('punkt')
```

### Issue: Port already in use
**Solution:** Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

---

## 📈 Roadmap

- [ ] Email/SMS alerts for high friction
- [ ] Multi-language support
- [ ] Advanced analytics (cohort analysis)
- [ ] Integration with CRM systems
- [ ] Mobile apps (iOS/Android)
- [ ] Export reports (PDF/Excel)
- [ ] Team collaboration features
- [ ] API for third-party integrations

---

## 🤝 Support

For questions or issues:
- Email: support@raypulse.com (example)
- Documentation: See this README
- GitHub Issues: (if applicable)

---

## 📄 License

This project is proprietary software. All rights reserved.

---

## 👥 Credits

**Developed By:** RayPulse Team
**Year:** 2026
**Technology:** Python, Flask, AI/ML, Bootstrap

---

## 🎉 Get Started

```bash
cd raypulse
pip install -r requirements.txt
python app.py
```

Visit **http://localhost:5000** and start detecting customer dissatisfaction!

---

**RayPulse** - *Turn Silent Customer Exits Into Business Growth* 🚀
