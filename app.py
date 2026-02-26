from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
import qrcode
from io import BytesIO
import base64
from database import db
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.chatbot import RayPulseAI

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raypulse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
sentiment_analyzer = SentimentAnalyzer()
chatbot = RayPulseAI()

# Import models after app initialization
from models.models import Business, Feedback, Alert, Payment, ChatMessage

@login_manager.user_loader
def load_user(user_id):
    return Business.query.get(int(user_id))

# ============ LANDING PAGE ============
@app.route('/')
def index():
    return render_template('index.html')

# ============ BUSINESS REGISTRATION ============
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        business_type = request.form.get('business_type')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if business already exists
        existing_business = Business.query.filter_by(email=email).first()
        if existing_business:
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('register'))

        # Generate unique company ID
        company_id = 'RP' + secrets.token_hex(6).upper()

        # Create new business
        new_business = Business(
            business_name=business_name,
            business_type=business_type,
            email=email,
            password_hash=generate_password_hash(password),
            company_id=company_id,
            feedback_url=f'/feedback/{company_id}'
        )

        db.session.add(new_business)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ============ BUSINESS LOGIN ============
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        business = Business.query.filter_by(email=email).first()

        if business and check_password_hash(business.password_hash, password):
            login_user(business)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

# ============ BUSINESS LOGOUT ============
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ============ CUSTOMER FEEDBACK PAGE ============
@app.route('/feedback/<company_id>', methods=['GET', 'POST'])
def feedback(company_id):
    business = Business.query.filter_by(company_id=company_id).first()

    if not business:
        return "Invalid feedback link", 404

    if request.method == 'POST':
        star_rating = request.form.get('star_rating')
        emotion = request.form.get('emotion')
        feedback_text = request.form.get('feedback_text', '')

        # Analyze sentiment
        sentiment_score = sentiment_analyzer.analyze(feedback_text)

        # Calculate friction score (0-100, higher = more friction)
        friction_score = calculate_friction_score(int(star_rating), emotion, sentiment_score)

        # Determine risk level
        risk_level = determine_risk_level(friction_score)

        # Save feedback
        new_feedback = Feedback(
            business_id=business.id,
            star_rating=int(star_rating),
            emotion=emotion,
            feedback_text=feedback_text,
            sentiment_score=sentiment_score,
            friction_score=friction_score,
            risk_level=risk_level
        )

        db.session.add(new_feedback)

        # Generate alert if high friction
        if friction_score >= 60:
            alert = Alert(
                business_id=business.id,
                alert_type='HIGH_FRICTION',
                message=f'High friction detected: {friction_score}/100',
                severity=risk_level
            )
            db.session.add(alert)

        db.session.commit()

        return render_template('feedback_success.html', business=business)

    return render_template('feedback.html', business=business, company_id=company_id)

# ============ BUSINESS DASHBOARD ============
@app.route('/dashboard')
@login_required
def dashboard():
    # Get all feedback for current business
    feedbacks = Feedback.query.filter_by(business_id=current_user.id).all()

    # Calculate metrics
    total_feedbacks = len(feedbacks)

    if total_feedbacks == 0:
        stats = {
            'total_feedbacks': 0,
            'avg_rating': 0,
            'avg_friction': 0,
            'high_risk_count': 0,
            'satisfaction_rate': 0
        }
    else:
        avg_rating = sum(f.star_rating for f in feedbacks) / total_feedbacks
        avg_friction = sum(f.friction_score for f in feedbacks) / total_feedbacks
        high_risk_count = len([f for f in feedbacks if f.risk_level == 'HIGH'])
        satisfaction_rate = len([f for f in feedbacks if f.star_rating >= 4]) / total_feedbacks * 100

        stats = {
            'total_feedbacks': total_feedbacks,
            'avg_rating': round(avg_rating, 2),
            'avg_friction': round(avg_friction, 2),
            'high_risk_count': high_risk_count,
            'satisfaction_rate': round(satisfaction_rate, 2)
        }

    # Get recent alerts
    alerts = Alert.query.filter_by(business_id=current_user.id).order_by(Alert.created_at.desc()).limit(5).all()

    # Get QR code
    qr_code_data = generate_qr_code(current_user.company_id)

    return render_template('dashboard.html',
                         business=current_user,
                         stats=stats,
                         feedbacks=feedbacks[-10:],
                         alerts=alerts,
                         qr_code=qr_code_data)

# ============ ALERTS & RECOMMENDATIONS ============
@app.route('/alerts')
@login_required
def alerts_page():
    alerts = Alert.query.filter_by(business_id=current_user.id).order_by(Alert.created_at.desc()).all()

    # Generate recommendations
    recommendations = generate_recommendations(current_user.id)

    return render_template('alerts.html', alerts=alerts, recommendations=recommendations)

# ============ API ENDPOINTS ============
@app.route('/api/dashboard-data')
@login_required
def dashboard_data():
    feedbacks = Feedback.query.filter_by(business_id=current_user.id).order_by(Feedback.created_at.desc()).limit(30).all()

    # Prepare data for charts
    dates = []
    ratings = []
    friction_scores = []

    for feedback in reversed(feedbacks):
        dates.append(feedback.created_at.strftime('%m/%d'))
        ratings.append(feedback.star_rating)
        friction_scores.append(feedback.friction_score)

    return jsonify({
        'dates': dates,
        'ratings': ratings,
        'friction_scores': friction_scores
    })

# ============ CHATBOT API ============
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chatbot conversations"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', secrets.token_hex(8))

    # Get AI response
    bot_response = chatbot.get_response(user_message)
    quick_replies = chatbot.get_quick_replies()

    # Save to database if user is logged in
    if current_user.is_authenticated:
        chat_record = ChatMessage(
            business_id=current_user.id,
            session_id=session_id,
            message=user_message,
            response=bot_response
        )
        db.session.add(chat_record)
        db.session.commit()

    return jsonify({
        'response': bot_response,
        'quick_replies': quick_replies,
        'session_id': session_id
    })

# ============ SUBSCRIPTION & PAYMENT ============
@app.route('/subscription')
@login_required
def subscription():
    """Subscription plans page"""
    return render_template('subscription.html', business=current_user)

@app.route('/subscribe/<plan>', methods=['POST'])
@login_required
def subscribe(plan):
    """Handle subscription selection"""
    # Pricing
    pricing = {
        'basic': 29.00,
        'pro': 99.00,
        'enterprise': 299.00
    }

    amount = pricing.get(plan, 0)

    if amount == 0:
        flash('Invalid subscription plan', 'error')
        return redirect(url_for('subscription'))

    # Create payment record
    payment = Payment(
        business_id=current_user.id,
        plan=plan,
        amount=amount,
        currency='USD',
        status='pending'
    )
    db.session.add(payment)
    db.session.commit()

    # Show payment QR code page
    return render_template('payment.html', plan=plan, amount=amount, payment_id=payment.id)

@app.route('/payment/confirm/<int:payment_id>', methods=['POST'])
@login_required
def confirm_payment(payment_id):
    """Confirm payment completion"""
    payment = Payment.query.get_or_404(payment_id)

    if payment.business_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))

    # Update payment status
    payment.status = 'completed'
    payment.transaction_id = secrets.token_hex(16)

    # Update business subscription
    current_user.subscription_plan = payment.plan
    current_user.subscription_status = 'active'
    current_user.subscription_start = datetime.utcnow()
    current_user.subscription_end = datetime.utcnow() + timedelta(days=30)

    db.session.commit()

    flash(f'Successfully subscribed to {payment.plan.upper()} plan!', 'success')
    return redirect(url_for('dashboard'))

# ============ HELPER FUNCTIONS ============
def calculate_friction_score(star_rating, emotion, sentiment_score):
    """Calculate friction score (0-100, higher = more friction)"""
    # Star rating component (inverted: 1 star = high friction)
    star_friction = (5 - star_rating) * 20

    # Emotion component
    emotion_friction = {
        'happy': 0,
        'neutral': 30,
        'unhappy': 70
    }.get(emotion, 30)

    # Sentiment component (negative sentiment = high friction)
    sentiment_friction = (1 - sentiment_score) * 100

    # Weighted average
    friction_score = (star_friction * 0.4) + (emotion_friction * 0.3) + (sentiment_friction * 0.3)

    return round(friction_score, 2)

def determine_risk_level(friction_score):
    """Determine risk level based on friction score"""
    if friction_score >= 60:
        return 'HIGH'
    elif friction_score >= 30:
        return 'MEDIUM'
    else:
        return 'LOW'

def generate_qr_code(company_id):
    """Generate QR code for feedback URL"""
    feedback_url = f"http://localhost:5000/feedback/{company_id}"

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(feedback_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"

def generate_recommendations(business_id):
    """Generate AI-powered recommendations based on feedback analysis"""
    feedbacks = Feedback.query.filter_by(business_id=business_id).all()

    if not feedbacks:
        return []

    # Analyze common issues
    high_friction_feedbacks = [f for f in feedbacks if f.friction_score >= 60]

    recommendations = []

    if len(high_friction_feedbacks) > len(feedbacks) * 0.3:
        recommendations.append({
            'type': 'CRITICAL',
            'title': 'High Customer Friction Detected',
            'description': f'{len(high_friction_feedbacks)} customers ({round(len(high_friction_feedbacks)/len(feedbacks)*100)}%) reported high friction',
            'action': 'Immediate investigation required. Review recent operational changes.'
        })

    # Low ratings analysis
    low_ratings = [f for f in feedbacks if f.star_rating <= 2]
    if len(low_ratings) > 5:
        recommendations.append({
            'type': 'WARNING',
            'title': 'Product/Service Quality Issues',
            'description': f'{len(low_ratings)} customers gave 2-star or lower ratings',
            'action': 'Review product quality, delivery process, and customer service protocols.'
        })

    # Positive feedback
    high_ratings = [f for f in feedbacks if f.star_rating >= 4]
    if len(high_ratings) > len(feedbacks) * 0.7:
        recommendations.append({
            'type': 'SUCCESS',
            'title': 'Strong Customer Satisfaction',
            'description': f'{round(len(high_ratings)/len(feedbacks)*100)}% of customers are satisfied',
            'action': 'Maintain current quality standards and consider scaling operations.'
        })

    return recommendations

# ============ DATABASE INITIALIZATION ============
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
