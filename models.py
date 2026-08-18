from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. Users table (Default user: user / 1234)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='student') # student, faculty, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 2. Complaint Management System
class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    reg_number = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(80), nullable=False) # Hostel, Mess, Lab, Academic, Transport, Infrastructure
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='Medium') # Low, Medium, High, Critical
    status = db.Column(db.String(20), default='Open') # Open, In-Progress, Resolved, Rejected
    admin_remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 3. Cloud File Management System
class CloudFile(db.Model):
    __tablename__ = 'cloud_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size_kb = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), default='General') # Notes, Assignment, Project, Circular, Research
    uploaded_by = db.Column(db.String(80), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 4. Student Performance Prediction AI
class StudentPrediction(db.Model):
    __tablename__ = 'student_predictions'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    roll_no = db.Column(db.String(50), nullable=False)
    attendance_pct = db.Column(db.Float, nullable=False)
    internal1_mark = db.Column(db.Float, nullable=False)
    internal2_mark = db.Column(db.Float, nullable=False)
    assignment_score = db.Column(db.Float, nullable=False)
    study_hours_per_day = db.Column(db.Float, nullable=False)
    predicted_grade = db.Column(db.String(10), nullable=False)
    predicted_gpa = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False) # Low Risk, Moderate Risk, High Risk
    ai_recommendations = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 5. Bus Tracking System
class BusRoute(db.Model):
    __tablename__ = 'bus_routes'
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(50), nullable=False) # e.g. VVK-BUS-07
    route_name = db.Column(db.String(120), nullable=False) # e.g. Tiruchengode - Erode Route
    driver_name = db.Column(db.String(100), nullable=False)
    driver_phone = db.Column(db.String(20), nullable=False)
    current_stop = db.Column(db.String(100), nullable=False)
    next_stop = db.Column(db.String(100), nullable=False)
    eta_minutes = db.Column(db.Integer, default=15)
    speed_kmph = db.Column(db.Float, default=42.0)
    status = db.Column(db.String(30), default='On-Time') # On-Time, Delayed, Reached Campus
    capacity_pct = db.Column(db.Integer, default=65)
    stops_json = db.Column(db.Text, nullable=True) # JSON list of stops with lat/lng/names
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 6. Headlines In India
class IndianHeadline(db.Model):
    __tablename__ = 'indian_headlines'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Technology, Higher Education, Sports, National, Business
    source = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    read_time = db.Column(db.String(20), default='3 min read')
    is_trending = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)

# 7. E-Commerce for Sports Products
class SportsProduct(db.Model):
    __tablename__ = 'sports_products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Cricket, Badminton, Football, Gym & Fitness, Athletics
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=4.5)
    stock_count = db.Column(db.Integer, default=25)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(80), nullable=False)

class SportsOrder(db.Model):
    __tablename__ = 'sports_orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    items_json = db.Column(db.Text, nullable=False) # JSON array of items
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='UPI')
    status = db.Column(db.String(30), default='Confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 8. AI Code Reviewer & Bug Fixer
class CodeReviewSession(db.Model):
    __tablename__ = 'code_review_sessions'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    submitted_code = db.Column(db.Text, nullable=False)
    bugs_detected = db.Column(db.Text, nullable=False)
    security_issues = db.Column(db.Text, nullable=False)
    fixed_code = db.Column(db.Text, nullable=False)
    optimization_score = db.Column(db.Integer, default=85)
    complexity = db.Column(db.String(20), default='O(N)')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 9. Student Assessment Using AI
class StudentAssessment(db.Model):
    __tablename__ = 'student_assessments'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    roll_no = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False) # Python & DSA, Web Technologies, Database Systems, AI & ML
    score = db.Column(db.Float, nullable=False)
    total_questions = db.Column(db.Integer, default=10)
    correct_answers = db.Column(db.Integer, nullable=False)
    time_taken_seconds = db.Column(db.Integer, nullable=False)
    strength_areas = db.Column(db.Text, nullable=False)
    improvement_areas = db.Column(db.Text, nullable=False)
    ai_feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 10. Customer Relationship Management (CRM) System
class CRMLead(db.Model):
    __tablename__ = 'crm_leads'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    deal_value = db.Column(db.Float, nullable=False)
    stage = db.Column(db.String(50), default='Lead') # Lead, Contacted, Proposal, Negotiation, Won, Lost
    lead_source = db.Column(db.String(50), default='Campus Outreach')
    assigned_to = db.Column(db.String(100), default='Placement & Industry Cell')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 11. Fake News Detection & Reporting System
class FakeNewsReport(db.Model):
    __tablename__ = 'fake_news_reports'
    id = db.Column(db.Integer, primary_key=True)
    news_title = db.Column(db.String(255), nullable=False)
    news_content = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(255), nullable=True)
    credibility_score = db.Column(db.Float, nullable=False) # 0 to 100%
    prediction = db.Column(db.String(30), nullable=False) # REAL / LEGITIMATE, HIGHLY SUSPICIOUS, FAKE / MISLEADING
    linguistic_cues = db.Column(db.Text, nullable=False)
    reported_by = db.Column(db.String(80), default='user')
    status = db.Column(db.String(30), default='Verified by AI')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 12. Gold & Silver Fake / Purity Detection
class MetalPurityTest(db.Model):
    __tablename__ = 'metal_purity_tests'
    id = db.Column(db.Integer, primary_key=True)
    metal_type = db.Column(db.String(20), nullable=False) # Gold / Silver
    weight_in_air_g = db.Column(db.Float, nullable=False)
    weight_in_water_g = db.Column(db.Float, nullable=False)
    calculated_density = db.Column(db.Float, nullable=False)
    hallmark_number = db.Column(db.String(50), nullable=True)
    acid_test_result = db.Column(db.String(50), default='No Reaction (Pass)')
    magnet_test = db.Column(db.String(50), default='Non-Magnetic (Pass)')
    estimated_karat = db.Column(db.String(20), nullable=False) # 24K, 22K, 18K, 14K, Fake/Plated
    purity_percentage = db.Column(db.Float, nullable=False)
    verdict = db.Column(db.String(50), nullable=False) # GENUINE, ALLOYED / IMPURE, SUSPECTED FAKE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 13. Cricket Club Management System
class CricketPlayer(db.Model):
    __tablename__ = 'cricket_players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False) # Batsman, Bowler, All-Rounder, Wicket Keeper
    batting_style = db.Column(db.String(50), default='Right Hand')
    matches_played = db.Column(db.Integer, default=12)
    runs_scored = db.Column(db.Integer, default=340)
    wickets_taken = db.Column(db.Integer, default=8)
    batting_avg = db.Column(db.Float, default=34.0)
    strike_rate = db.Column(db.Float, default=128.5)
    team_name = db.Column(db.String(100), default='Vivekanandha Warriors')

class CricketMatch(db.Model):
    __tablename__ = 'cricket_matches'
    id = db.Column(db.Integer, primary_key=True)
    match_title = db.Column(db.String(150), nullable=False)
    team1 = db.Column(db.String(100), nullable=False)
    team2 = db.Column(db.String(100), nullable=False)
    venue = db.Column(db.String(120), default='VVK Central Grounds')
    match_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Upcoming') # Live, Completed, Upcoming
    score_team1 = db.Column(db.String(50), default='-')
    score_team2 = db.Column(db.String(50), default='-')
    result = db.Column(db.String(150), default='Match scheduled')

# 14. Two-Wheeler Service & Maintenance
class TwoWheelerService(db.Model):
    __tablename__ = 'two_wheeler_services'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    bike_model = db.Column(db.String(100), nullable=False) # e.g. Yamaha R15, Royal Enfield 350, Honda Activa 6G
    vehicle_number = db.Column(db.String(50), nullable=False) # e.g. TN-34-AZ-2026
    service_type = db.Column(db.String(50), nullable=False) # General Service, Engine Oil Change, Brake Overhaul, Full Restoration
    issues_reported = db.Column(db.Text, nullable=False)
    estimated_cost = db.Column(db.Float, nullable=False)
    service_status = db.Column(db.String(30), default='Vehicle Received') # Received, In-Progress, Quality Check, Ready for Delivery, Delivered
    mechanic_assigned = db.Column(db.String(80), default='Master Tech S. Kumar')
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

# 15. Intercollegiate Registration Management
class IntercollegeRegistration(db.Model):
    __tablename__ = 'intercollege_registrations'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(80), unique=True, nullable=False) # e.g. VVK-FEST-9821
    participant_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    college_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    event_category = db.Column(db.String(150), nullable=False)
    team_size = db.Column(db.Integer, default=1)
    team_members = db.Column(db.Text, nullable=True)
    payment_status = db.Column(db.String(100), default='Registered (Free / Confirmed)')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
