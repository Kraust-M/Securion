from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class SecurityAssessmentForm(FlaskForm):
    """Security assessment form"""
    password_strength = RadioField(
        'How strong are your passwords?',
        choices=[
            (1, 'Very weak (short, simple passwords)'),
            (2, 'Weak (longer but simple passwords)'),
            (3, 'Moderate (mix of characters but same across sites)'),
            (4, 'Strong (complex passwords, different for important sites)'),
            (5, 'Very strong (complex, unique passwords for each site)')
        ],
        validators=[DataRequired()]
    )
    
    two_factor = BooleanField('Do you use two-factor authentication for important accounts?')
    
    device_encryption = BooleanField('Are your devices (phone, computer) encrypted?')
    
    update_frequency = SelectField(
        'How often do you update your devices and software?',
        choices=[
            ('never', 'Never or almost never'),
            ('rarely', 'Rarely (when forced to)'),
            ('sometimes', 'Sometimes (occasionally when reminded)'),
            ('regularly', 'Regularly (as soon as updates are available)')
        ],
        validators=[DataRequired()]
    )
    
    backup_frequency = SelectField(
        'How often do you back up your important data?',
        choices=[
            ('never', 'Never'),
            ('rarely', 'Rarely (less than once a year)'),
            ('sometimes', 'Sometimes (a few times a year)'),
            ('regularly', 'Regularly (monthly or more frequently)')
        ],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Complete Assessment') 