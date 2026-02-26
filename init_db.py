"""
Database Initialization Script for RayPulse
This script creates all necessary database tables
"""

from app import app, db
from models.models import Business, Feedback, Alert

def init_database():
    """Initialize the database and create all tables"""
    with app.app_context():
        # Drop all tables (use with caution in production)
        # db.drop_all()

        # Create all tables
        db.create_all()

        print("=" * 50)
        print("✓ Database initialized successfully!")
        print("✓ Tables created: businesses, feedbacks, alerts")
        print("=" * 50)
        print("\nRayPulse is ready to use!")
        print("Run 'python app.py' to start the server")
        print("=" * 50)

if __name__ == '__main__':
    init_database()
