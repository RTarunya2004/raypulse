# RayPulse - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

**Manual Installation:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate.bat

# Install dependencies
pip install Flask Flask-SQLAlchemy Flask-Login qrcode textblob nltk

# Download NLTK data
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"

# Initialize database
python init_db.py
```

---

### Step 2: Start the Server

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Run the application
python app.py
```

The server will start at: **http://localhost:5000**

---

### Step 3: Register Your Business

1. Open browser: **http://localhost:5000**
2. Click "Get Started" or "Register"
3. Fill in your business details:
   - Business Name: e.g., "Acme Manufacturing"
   - Business Type: Select from dropdown
   - Email: your@email.com
   - Password: Create a secure password
4. Click "Create Account"

**System Auto-Generates:**
- ✅ Unique Company ID (e.g., RP4A2B3C4D5E6F)
- ✅ Feedback URL
- ✅ QR Code for customer feedback

---

## 📱 Test the Complete Workflow

### 1. Login to Dashboard
- Email: the email you registered with
- Password: your password
- Click "Login"

### 2. Get Your Feedback QR Code
- On dashboard, scroll to "Your Feedback QR Code"
- Right-click QR code → Save Image
- Or copy the feedback URL

### 3. Test Customer Feedback
- Open the feedback URL in a new browser window/incognito
- Format: `http://localhost:5000/feedback/YOUR_COMPANY_ID`
- Fill out the feedback form:
  - Rate with stars (1-5)
  - Select emotion (😊 😐 😡)
  - Add optional comment
  - Submit

### 4. View Analytics
- Go back to dashboard
- See real-time feedback appear
- Check friction scores
- View alerts (if high friction detected)
- Explore charts and trends

### 5. Check AI Recommendations
- Click "Alerts" in navigation
- View AI-powered recommendations
- See friction patterns
- Get actionable insights

---

## 🎯 Use Case Example

**Scenario: Factory Testing**

1. **Register** your factory business
2. **Print** the QR code
3. **Attach** QR code to product packaging
4. **Ask** a colleague to scan and submit test feedback:
   - Try different ratings (1-5 stars)
   - Try different emotions
   - Add comments like "delivery was late" or "great quality"
5. **Monitor** dashboard to see:
   - Feedback appear in real-time
   - Friction scores calculated
   - Alerts triggered for low ratings
   - AI recommendations generated

---

## 📊 Understanding the Metrics

### Friction Score (0-100)
- **0-29 (LOW)**: Customer is satisfied ✅
- **30-59 (MEDIUM)**: Some concerns, monitor closely ⚠️
- **60-100 (HIGH)**: High risk of customer loss! Take action ⛔

### Risk Levels
- **HIGH**: Immediate attention required
- **MEDIUM**: Plan improvements
- **LOW**: Maintain quality

### Dashboard Metrics
- **Total Feedback**: All customer responses received
- **Avg Rating**: Average star rating (1-5)
- **High Risk Alerts**: Number of high-friction alerts
- **Satisfaction Rate**: % of customers rating 4+ stars

---

## 🔧 Troubleshooting

### Issue: Cannot access http://localhost:5000
**Solution:** Make sure the Flask app is running. Check terminal for errors.

### Issue: Database not found
**Solution:** Run `python init_db.py` to create database.

### Issue: QR code not displaying
**Solution:** Check that `qrcode` package is installed: `pip install qrcode`

### Issue: Sentiment analysis errors
**Solution:** Download NLTK data:
```python
import nltk
nltk.download('brown')
nltk.download('punkt')
```

### Issue: Port 5000 already in use
**Solution:** Change port in app.py (line at bottom):
```python
app.run(debug=True, port=5001)  # Use different port
```

---

## 🎨 Customization

### Change Brand Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;  /* Your brand color */
    --secondary-color: #764ba2;
}
```

### Change Company Name in UI
Edit templates (index.html, base.html) to replace "RayPulse" with your brand.

### Add Logo
Place logo in `static/images/logo.png` and update navbar in `base.html`.

---

## 📁 Project Structure

```
raypulse/
├── app.py              # Main Flask application
├── database.py         # Database configuration
├── init_db.py          # Database initialization
├── requirements.txt    # Python dependencies
├── models/
│   └── models.py      # Data models
├── utils/
│   └── sentiment_analyzer.py  # AI engine
├── templates/         # HTML templates
├── static/
│   └── css/
│       └── style.css  # Custom styles
└── raypulse.db       # SQLite database (created after init)
```

---

## 🚀 Next Steps

1. **Deploy to Production**
   - Use PostgreSQL/MySQL instead of SQLite
   - Set up HTTPS/SSL
   - Use environment variables for secrets
   - Deploy on cloud (AWS, Azure, Heroku)

2. **Add Features**
   - Email notifications
   - SMS alerts
   - Export reports (PDF/Excel)
   - Multi-language support

3. **Integrate with Existing Systems**
   - CRM integration
   - API for third-party apps
   - Webhook notifications

---

## 💡 Pro Tips

1. **Test with Different Feedback**
   - Try 1-star ratings → See HIGH risk alerts
   - Try 5-star ratings → See LOW risk
   - Add negative comments → Watch sentiment analysis

2. **Print Multiple QR Codes**
   - Different locations
   - Different products
   - Track where feedback comes from

3. **Monitor Regularly**
   - Check dashboard daily
   - Act on high-friction alerts immediately
   - Track trends over time

---

## 🎉 You're Ready!

Your RayPulse platform is now set up and ready to detect customer dissatisfaction early and convert insights into business growth.

**Support:** For questions, check README.md for detailed documentation.

---

**RayPulse** - *Turn Silent Customer Exits Into Business Growth* 🚀
