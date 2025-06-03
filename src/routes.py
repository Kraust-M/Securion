from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .app import app
from .models import User, SecurityTip, SecurityAssessment
from .forms import LoginForm, RegisterForm, SecurityAssessmentForm

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Create new user
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        user.save()
        
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    tips = SecurityTip.get_random_tips(3)  # Get 3 random security tips
    return render_template('dashboard.html', tips=tips)

@app.route('/security-assessment', methods=['GET', 'POST'])
@login_required
def security_assessment():
    """Security assessment route"""
    form = SecurityAssessmentForm()
    if form.validate_on_submit():
        assessment = SecurityAssessment(
            user_id=current_user.id,
            password_strength=form.password_strength.data,
            two_factor=form.two_factor.data,
            device_encryption=form.device_encryption.data,
            update_frequency=form.update_frequency.data,
            backup_frequency=form.backup_frequency.data
        )
        assessment.save()
        
        # Calculate security score
        score = assessment.calculate_score()
        
        return redirect(url_for('assessment_results', assessment_id=assessment.id))
    
    return render_template('security_assessment.html', form=form)

@app.route('/assessment-results/<int:assessment_id>')
@login_required
def assessment_results(assessment_id):
    """Show results of security assessment"""
    assessment = SecurityAssessment.query.get_or_404(assessment_id)
    
    # Ensure user can only view their own assessments
    if assessment.user_id != current_user.id:
        flash('You do not have permission to view this assessment', 'danger')
        return redirect(url_for('dashboard'))
    
    score = assessment.calculate_score()
    recommendations = assessment.get_recommendations()
    
    return render_template('assessment_results.html', 
                          assessment=assessment, 
                          score=score,
                          recommendations=recommendations)

@app.route('/learning')
@login_required
def learning():
    """Security learning resources"""
    return render_template('learning.html')

@app.route('/security-tips')
def security_tips():
    """Security tips page"""
    tips = SecurityTip.query.all()
    return render_template('security_tips.html', tips=tips) 