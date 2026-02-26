"""
Create Demo Data for RayPulse
This script creates sample feedback data for testing purposes
"""

from app import app, db
from models.models import Business, Feedback, Alert
from werkzeug.security import generate_password_hash
from utils.sentiment_analyzer import SentimentAnalyzer
from datetime import datetime, timedelta
import random
import secrets

def create_demo_business():
    """Create a demo business account"""
    with app.app_context():
        # Check if demo business exists
        demo_business = Business.query.filter_by(email='demo@raypulse.com').first()

        if demo_business:
            print("Demo business already exists!")
            print(f"Email: demo@raypulse.com")
            print(f"Password: demo123")
            print(f"Company ID: {demo_business.company_id}")
            return demo_business

        # Create demo business
        company_id = 'RPDEMO' + secrets.token_hex(4).upper()

        demo_business = Business(
            business_name='Acme Manufacturing Demo',
            business_type='Manufacturing',
            email='demo@raypulse.com',
            password_hash=generate_password_hash('demo123'),
            company_id=company_id,
            feedback_url=f'/feedback/{company_id}'
        )

        db.session.add(demo_business)
        db.session.commit()

        print("=" * 50)
        print("✓ Demo business created successfully!")
        print("=" * 50)
        print(f"Email: demo@raypulse.com")
        print(f"Password: demo123")
        print(f"Company ID: {company_id}")
        print("=" * 50)

        return demo_business

def create_demo_feedback(business):
    """Create sample feedback data"""
    with app.app_context():
        sentiment_analyzer = SentimentAnalyzer()

        # Sample feedback scenarios
        feedback_scenarios = [
            {'rating': 5, 'emotion': 'happy', 'text': 'Excellent product quality! Very satisfied with my purchase.'},
            {'rating': 5, 'emotion': 'happy', 'text': 'Fast delivery and great customer service.'},
            {'rating': 4, 'emotion': 'happy', 'text': 'Good quality but slightly expensive.'},
            {'rating': 4, 'emotion': 'neutral', 'text': 'Product is fine, delivery could be faster.'},
            {'rating': 3, 'emotion': 'neutral', 'text': 'Average experience, nothing special.'},
            {'rating': 3, 'emotion': 'neutral', 'text': 'Product is okay but packaging was damaged.'},
            {'rating': 2, 'emotion': 'unhappy', 'text': 'Delivery was late by 3 days.'},
            {'rating': 2, 'emotion': 'unhappy', 'text': 'Product quality is poor, not worth the price.'},
            {'rating': 1, 'emotion': 'unhappy', 'text': 'Terrible experience! Product arrived broken and customer service did not respond.'},
            {'rating': 1, 'emotion': 'unhappy', 'text': 'Very disappointed. Wrong item was delivered.'},
            {'rating': 5, 'emotion': 'happy', 'text': 'Amazing! Exceeded my expectations.'},
            {'rating': 4, 'emotion': 'happy', 'text': 'Very good, will order again.'},
            {'rating': 3, 'emotion': 'neutral', 'text': 'Meets basic requirements.'},
            {'rating': 2, 'emotion': 'unhappy', 'text': 'Poor quality control, defective product.'},
            {'rating': 5, 'emotion': 'happy', 'text': 'Perfect! Highly recommend.'},
        ]

        # Create feedback entries with dates spread over last 7 days
        for i, scenario in enumerate(feedback_scenarios):
            # Calculate friction score
            sentiment_score = sentiment_analyzer.analyze(scenario['text'])

            star_friction = (5 - scenario['rating']) * 20
            emotion_friction = {'happy': 0, 'neutral': 30, 'unhappy': 70}[scenario['emotion']]
            sentiment_friction = (1 - sentiment_score) * 100
            friction_score = (star_friction * 0.4) + (emotion_friction * 0.3) + (sentiment_friction * 0.3)

            # Determine risk level
            if friction_score >= 60:
                risk_level = 'HIGH'
            elif friction_score >= 30:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'

            # Create feedback with past dates
            days_ago = len(feedback_scenarios) - i - 1
            created_date = datetime.utcnow() - timedelta(days=days_ago // 2, hours=days_ago % 2 * 12)

            feedback = Feedback(
                business_id=business.id,
                star_rating=scenario['rating'],
                emotion=scenario['emotion'],
                feedback_text=scenario['text'],
                sentiment_score=sentiment_score,
                friction_score=round(friction_score, 2),
                risk_level=risk_level,
                created_at=created_date
            )

            db.session.add(feedback)

            # Create alert for high friction
            if friction_score >= 60:
                alert = Alert(
                    business_id=business.id,
                    alert_type='HIGH_FRICTION',
                    message=f'High friction detected: {round(friction_score, 2)}/100',
                    severity=risk_level,
                    created_at=created_date
                )
                db.session.add(alert)

        db.session.commit()

        print(f"✓ Created {len(feedback_scenarios)} demo feedback entries")
        print("✓ Created high-friction alerts")
        print("=" * 50)

def main():
    """Main function to create all demo data"""
    print("\nCreating RayPulse Demo Data...")
    print("=" * 50)

    create_demo_business()

    # Get business from DB
    with app.app_context():
        business = Business.query.filter_by(email='demo@raypulse.com').first()
        create_demo_feedback(business)

    print("\n✓ Demo data created successfully!")
    print("\nYou can now:")
    print("1. Login with: demo@raypulse.com / demo123")
    print("2. View dashboard with sample feedback")
    print("3. Test the feedback URL with your Company ID")
    print("=" * 50)

if __name__ == '__main__':
    main()
