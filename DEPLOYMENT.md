# RayPulse - Production Deployment Guide

## 🚀 Production Deployment Options

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Create Heroku App**
```bash
heroku login
heroku create raypulse-app
```

3. **Add PostgreSQL Database**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Create Procfile**
```
web: gunicorn app:app
```

5. **Update requirements.txt**
```bash
echo "gunicorn" >> requirements.txt
echo "psycopg2-binary" >> requirements.txt
```

6. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku master
```

7. **Initialize Database**
```bash
heroku run python init_db.py
```

---

### Option 2: Deploy to AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro or larger
   - Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **Connect to Server**
```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

3. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

4. **Upload Code**
```bash
scp -r raypulse ubuntu@your-server-ip:/home/ubuntu/
```

5. **Setup Application**
```bash
cd /home/ubuntu/raypulse
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
python init_db.py
```

6. **Create Systemd Service** (`/etc/systemd/system/raypulse.service`)
```ini
[Unit]
Description=RayPulse Flask Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/raypulse
Environment="PATH=/home/ubuntu/raypulse/venv/bin"
ExecStart=/home/ubuntu/raypulse/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

7. **Configure Nginx** (`/etc/nginx/sites-available/raypulse`)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

8. **Enable and Start Services**
```bash
sudo systemctl enable raypulse
sudo systemctl start raypulse
sudo ln -s /etc/nginx/sites-available/raypulse /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

9. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Option 3: Deploy to DigitalOcean App Platform

1. **Connect Repository**
   - Upload code to GitHub
   - Connect to DigitalOcean App Platform

2. **Configure App**
   - Runtime: Python 3.10+
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn -w 4 app:app`

3. **Add PostgreSQL Database**
   - Add managed PostgreSQL database
   - Auto-configure DATABASE_URL

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

---

## 🔒 Production Security Checklist

### 1. Environment Variables

Create `.env` file (DO NOT commit to git):
```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/raypulse
FLASK_ENV=production
```

Update `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///raypulse.db')
```

### 2. Database Migration

Switch from SQLite to PostgreSQL:
```python
# app.py
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
```

Install PostgreSQL:
```bash
pip install psycopg2-binary
```

### 3. HTTPS/SSL

Always use HTTPS in production:
- Use Cloudflare SSL
- Let's Encrypt (free)
- AWS Certificate Manager

### 4. Disable Debug Mode

```python
# app.py
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
```

### 5. Password Security

Already implemented:
- ✅ Werkzeug password hashing
- ✅ Salted passwords
- ✅ Secure session management

### 6. CORS Configuration

If building separate frontend:
```bash
pip install flask-cors
```

```python
from flask_cors import CORS
CORS(app, origins=['https://yourdomain.com'])
```

### 7. Rate Limiting

Prevent abuse:
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])
```

---

## 📊 Database Backups

### Automated Backups

**PostgreSQL:**
```bash
# Daily backup cron job
0 2 * * * pg_dump raypulse > /backups/raypulse_$(date +\%Y\%m\%d).sql
```

**SQLite:**
```bash
# Daily backup
0 2 * * * cp /path/to/raypulse.db /backups/raypulse_$(date +\%Y\%m\%d).db
```

---

## 🔍 Monitoring & Logging

### 1. Application Logging

Add to `app.py`:
```python
import logging

logging.basicConfig(filename='raypulse.log', level=logging.INFO)
```

### 2. Error Tracking

Use Sentry:
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
)
```

### 3. Uptime Monitoring

Use services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

---

## ⚡ Performance Optimization

### 1. Use Production Server

Replace Flask development server with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. Enable Caching

```bash
pip install Flask-Caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/dashboard')
@cache.cached(timeout=60)
def dashboard():
    # Cached for 60 seconds
```

### 3. Database Connection Pooling

```python
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
```

### 4. Static File CDN

Use CDN for Bootstrap, Chart.js:
- Cloudflare CDN
- AWS CloudFront
- Fastly

---

## 📧 Email Notifications

### Setup Email Alerts

```bash
pip install Flask-Mail
```

```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

def send_alert_email(business, alert):
    msg = Message('RayPulse Alert: High Friction Detected',
                  sender='noreply@raypulse.com',
                  recipients=[business.email])
    msg.body = f"Alert: {alert.message}"
    mail.send(msg)
```

---

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          ssh user@server "cd /path/to/raypulse && git pull && systemctl restart raypulse"
```

---

## 🌐 Custom Domain Setup

1. **Purchase Domain** (Namecheap, GoDaddy, Google Domains)

2. **Configure DNS**
```
Type    Name    Value
A       @       your-server-ip
A       www     your-server-ip
```

3. **Update Nginx**
```nginx
server_name raypulse.com www.raypulse.com;
```

4. **Setup SSL**
```bash
sudo certbot --nginx -d raypulse.com -d www.raypulse.com
```

---

## 📱 Mobile Optimization

Already implemented:
- ✅ Bootstrap responsive design
- ✅ Mobile-first feedback form
- ✅ Touch-friendly star ratings

---

## 🧪 Pre-Deployment Testing

```bash
# Run tests
python -m pytest

# Check security
pip install safety
safety check

# Load testing
pip install locust
locust -f load_test.py
```

---

## 🚨 Disaster Recovery

### 1. Database Backup Restoration

```bash
# PostgreSQL
psql raypulse < backup.sql

# SQLite
cp backup.db raypulse.db
```

### 2. Code Rollback

```bash
git log
git checkout <previous-commit-hash>
sudo systemctl restart raypulse
```

---

## 📊 Scaling Strategies

### Vertical Scaling
- Upgrade server resources (CPU, RAM)
- Increase database connections

### Horizontal Scaling
- Load balancer (Nginx, HAProxy)
- Multiple application servers
- Database replication

### Managed Services
- AWS RDS (Database)
- AWS Elastic Beanstalk (Application)
- Redis (Caching)

---

## ✅ Post-Deployment Checklist

- [ ] HTTPS enabled
- [ ] Debug mode disabled
- [ ] Environment variables configured
- [ ] Database backups automated
- [ ] Monitoring setup
- [ ] Error tracking enabled
- [ ] Email notifications working
- [ ] Custom domain configured
- [ ] SSL certificate valid
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation updated

---

## 🎉 Your RayPulse Platform is Production-Ready!

For support: support@raypulse.com (example)

---

**RayPulse** - *Turn Silent Customer Exits Into Business Growth* 🚀
