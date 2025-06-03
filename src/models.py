from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import hashlib
from .app import db

class User(UserMixin, db.Model):
    """User model for authentication and profile information"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('SecurityAssessment', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set the user password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        """Save user to database"""
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'


class SecurityTip(db.Model):
    """Security tips for users"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_random_tips(cls, count=3):
        """Get random security tips"""
        tips = cls.query.all()
        if len(tips) <= count:
            return tips
        return random.sample(tips, count)
    
    def __repr__(self):
        return f'<SecurityTip {self.title}>'


class SecurityAssessment(db.Model):
    """User security assessments"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Assessment questions
    password_strength = db.Column(db.Integer, nullable=False)  # 1-5 scale
    two_factor = db.Column(db.Boolean, default=False)
    device_encryption = db.Column(db.Boolean, default=False)
    update_frequency = db.Column(db.String(20), nullable=False)  # never, rarely, sometimes, regularly
    backup_frequency = db.Column(db.String(20), nullable=False)  # never, rarely, sometimes, regularly
    
    def calculate_score(self):
        """Calculate security score based on assessment answers"""
        score = 0
        
        # Password strength (1-5 scale)
        score += self.password_strength * 10
        
        # Two-factor authentication
        if self.two_factor:
            score += 20
        
        # Device encryption
        if self.device_encryption:
            score += 20
        
        # Update frequency
        if self.update_frequency == 'regularly':
            score += 20
        elif self.update_frequency == 'sometimes':
            score += 10
        elif self.update_frequency == 'rarely':
            score += 5
        
        # Backup frequency
        if self.backup_frequency == 'regularly':
            score += 20
        elif self.backup_frequency == 'sometimes':
            score += 10
        elif self.backup_frequency == 'rarely':
            score += 5
        
        return min(score, 100)  # Cap at 100
    
    def get_recommendations(self):
        """Get security recommendations based on assessment"""
        recommendations = []
        
        if self.password_strength < 3:
            recommendations.append({
                'title': 'Improve Password Strength',
                'content': 'Consider using longer passwords with a mix of uppercase, lowercase, numbers, and special characters.'
            })
        
        if not self.two_factor:
            recommendations.append({
                'title': 'Enable Two-Factor Authentication',
                'content': 'Two-factor authentication adds an extra layer of security to your accounts.'
            })
        
        if not self.device_encryption:
            recommendations.append({
                'title': 'Enable Device Encryption',
                'content': 'Encrypting your devices protects your data if they are lost or stolen.'
            })
        
        if self.update_frequency in ['never', 'rarely']:
            recommendations.append({
                'title': 'Update Your Software Regularly',
                'content': 'Regular updates patch security vulnerabilities and keep your devices secure.'
            })
        
        if self.backup_frequency in ['never', 'rarely']:
            recommendations.append({
                'title': 'Back Up Your Data Regularly',
                'content': 'Regular backups protect your data from loss due to hardware failure, theft, or ransomware.'
            })
        
        return recommendations
    
    def save(self):
        """Save assessment to database"""
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<SecurityAssessment {self.id} for User {self.user_id}>' 