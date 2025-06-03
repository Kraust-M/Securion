"""
Run the Securion application
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app import app
from src.models import db, User, SecurityTip

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Add sample security tips if none exist
        if SecurityTip.query.count() == 0:
            tips = [
                {
                    'title': 'Use a Password Manager',
                    'content': 'Use a password manager to generate and store strong, unique passwords for each account.',
                    'category': 'passwords',
                    'difficulty': 'beginner'
                },
                {
                    'title': 'Enable Two-Factor Authentication',
                    'content': 'Enable two-factor authentication on all accounts that support it for an extra layer of security.',
                    'category': 'passwords',
                    'difficulty': 'beginner'
                },
                {
                    'title': 'Keep Software Updated',
                    'content': 'Regularly update your operating system and applications to protect against security vulnerabilities.',
                    'category': 'devices',
                    'difficulty': 'beginner'
                },
                {
                    'title': 'Use a VPN on Public Wi-Fi',
                    'content': 'Always use a VPN when connecting to public Wi-Fi networks to encrypt your traffic.',
                    'category': 'network',
                    'difficulty': 'intermediate'
                },
                {
                    'title': 'Encrypt Your Devices',
                    'content': 'Enable full-disk encryption on all your devices to protect your data if they are lost or stolen.',
                    'category': 'devices',
                    'difficulty': 'intermediate'
                },
                {
                    'title': 'Use Secure Messaging Apps',
                    'content': 'Use end-to-end encrypted messaging apps for sensitive communications.',
                    'category': 'privacy',
                    'difficulty': 'intermediate'
                },
                {
                    'title': 'Set Up Email Filtering',
                    'content': 'Configure email filtering rules to reduce the risk of phishing attacks.',
                    'category': 'email',
                    'difficulty': 'advanced'
                },
                {
                    'title': 'Use Privacy-Focused Browser Extensions',
                    'content': 'Install browser extensions like uBlock Origin, Privacy Badger, and HTTPS Everywhere to enhance your privacy while browsing.',
                    'category': 'browsing',
                    'difficulty': 'intermediate'
                },
                {
                    'title': 'Secure Your Home Router',
                    'content': 'Change default router credentials, enable WPA3 encryption, and keep firmware updated.',
                    'category': 'network',
                    'difficulty': 'intermediate'
                },
                {
                    'title': 'Review App Permissions',
                    'content': 'Regularly review and limit the permissions granted to mobile apps and browser extensions.',
                    'category': 'privacy',
                    'difficulty': 'beginner'
                },
                {
                    'title': 'Use a Secure DNS Provider',
                    'content': 'Configure your devices to use a privacy-focused DNS provider like Quad9 or Cloudflare.',
                    'category': 'network',
                    'difficulty': 'advanced'
                },
                {
                    'title': 'Create Regular Backups',
                    'content': 'Back up your important data regularly using the 3-2-1 strategy: 3 copies, 2 different media types, 1 offsite.',
                    'category': 'devices',
                    'difficulty': 'beginner'
                }
            ]
            
            for tip_data in tips:
                tip = SecurityTip(
                    title=tip_data['title'],
                    content=tip_data['content'],
                    category=tip_data['category'],
                    difficulty=tip_data['difficulty']
                )
                db.session.add(tip)
            
            # Add demo user
            if User.query.filter_by(email='demo@securion.com').count() == 0:
                demo_user = User(
                    username='demo',
                    email='demo@securion.com'
                )
                demo_user.set_password('securepassword')
                db.session.add(demo_user)
            
            db.session.commit()
            print('Database initialized with sample data')

if __name__ == '__main__':
    # Initialize the database with sample data
    init_db()
    
    # Run the application
    app.run(debug=True) 