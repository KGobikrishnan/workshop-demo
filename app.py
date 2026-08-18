import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from models import (
    db, User, Complaint, CloudFile, StudentPrediction, BusRoute, IndianHeadline,
    SportsProduct, SportsOrder, CodeReviewSession, StudentAssessment, CRMLead,
    FakeNewsReport, MetalPurityTest, CricketPlayer, CricketMatch, TwoWheelerService,
    IntercollegeRegistration
)
from seed import seed_database
from ai_engine import predict_student_performance, analyze_code_with_ai, detect_fake_news_ai, calculate_metal_purity, evaluate_assessment_with_gemini

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# Initialize database tables and seed
with app.app_context():
    try:
        db.create_all()
        seed_database()
    except Exception as e:
        print(f"DB Init Warning: {e}")

# Helper decorator for authentication
def login_required_custom(f):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Context processor for global templates
@app.context_processor
def inject_global_data():
    return {
        'current_user': session.get('user', None),
        'user_role': session.get('role', 'Student'),
        'app_year': datetime.now().year,
        'app_name': 'Vivekanandha College Multi-Project Innovation Portal'
    }

# ==========================================
# 🔐 AUTHENTICATION ROUTES (user / 1234)
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Specific user requirement check: user / 1234
        if (username == 'user' and password == '1234') or (username == 'admin' and password == 'admin'):
            session['user'] = username
            session['role'] = 'Administrator' if username == 'admin' else 'VVK Scholar'
            flash(f"Welcome back, {username}! Access granted to VVK Multi-Project Hub.", "success")
            return redirect(url_for('dashboard'))
            
        user_record = User.query.filter_by(username=username).first()
        if user_record and check_password_hash(user_record.password, password):
            session['user'] = user_record.username
            session['role'] = user_record.role
            flash("Login Successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials! Use Username: 'user' and Password: '1234'", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out securely.", "info")
    return redirect(url_for('login'))

# ==========================================
# 📊 MASTER DASHBOARD
# ==========================================

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required_custom
def dashboard():
    # Gather key metrics for the summary cards
    stats = {
        'total_complaints': Complaint.query.count(),
        'open_complaints': Complaint.query.filter_by(status='Open').count(),
        'total_files': CloudFile.query.count(),
        'active_buses': BusRoute.query.count(),
        'sports_products': SportsProduct.query.count(),
        'code_reviews': CodeReviewSession.query.count(),
        'assessments_taken': StudentAssessment.query.count(),
        'crm_leads': CRMLead.query.count(),
        'event_registrations': IntercollegeRegistration.query.count(),
        'active_services': TwoWheelerService.query.count()
    }
    recent_complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(3).all()
    recent_registrations = IntercollegeRegistration.query.order_by(IntercollegeRegistration.created_at.desc()).limit(3).all()
    recent_predictions = StudentPrediction.query.order_by(StudentPrediction.created_at.desc()).limit(3).all()
    
    return render_template('dashboard.html', stats=stats, complaints=recent_complaints, registrations=recent_registrations, predictions=recent_predictions)

# ==========================================
# 1. 📢 COMPLAINT MANAGEMENT SYSTEM
# ==========================================

@app.route('/complaints', methods=['GET', 'POST'])
@login_required_custom
def complaints():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        reg_number = request.form.get('reg_number')
        department = request.form.get('department')
        category = request.form.get('category')
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'Medium')
        
        new_complaint = Complaint(
            student_name=student_name, reg_number=reg_number,
            department=department, category=category,
            title=title, description=description, priority=priority,
            status='Open'
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash("Your grievance has been lodged successfully and assigned an official tracking ticket!", "success")
        return redirect(url_for('complaints'))
        
    all_complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('modules/complaint.html', complaints=all_complaints)

@app.route('/api/complaints/<int:id>/status', methods=['POST'])
@login_required_custom
def update_complaint_status(id):
    c = Complaint.query.get_or_404(id)
    data = request.get_json() or {}
    c.status = data.get('status', c.status)
    c.admin_remark = data.get('admin_remark', c.admin_remark)
    db.session.commit()
    return jsonify({"success": True, "message": "Complaint status updated!"})

# ==========================================
# 2. ☁️ CLOUD FILE MANAGEMENT SYSTEM
# ==========================================

@app.route('/cloud-files', methods=['GET', 'POST'])
@login_required_custom
def cloud_files():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file chosen for upload!", "warning")
            return redirect(url_for('cloud_files'))
        uploaded_file = request.files['file']
        category = request.form.get('category', 'General')
        
        if uploaded_file.filename != '':
            original_name = uploaded_file.filename
            unique_name = f"{uuid.uuid4().hex[:8]}_{secure_filename(original_name)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            uploaded_file.save(filepath)
            
            size_kb = round(os.path.getsize(filepath) / 1024.0, 2)
            ext = original_name.split('.')[-1].upper() if '.' in original_name else 'FILE'
            
            new_file = CloudFile(
                filename=unique_name, original_name=original_name,
                file_type=f"{ext} Document", file_size_kb=size_kb,
                category=category, uploaded_by=session.get('user', 'user')
            )
            db.session.add(new_file)
            db.session.commit()
            flash(f"File '{original_name}' stored securely on VVK Cloud Nodes!", "success")
            return redirect(url_for('cloud_files'))
            
    files = CloudFile.query.order_by(CloudFile.created_at.desc()).all()
    total_storage_mb = round(sum(f.file_size_kb for f in files) / 1024.0, 2)
    return render_template('modules/cloud_files.html', files=files, total_storage_mb=total_storage_mb)

@app.route('/cloud-files/download/<int:file_id>')
@login_required_custom
def download_cloud_file(file_id):
    f = CloudFile.query.get_or_404(file_id)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    if os.path.exists(filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], f.filename, as_attachment=True, download_name=f.original_name)
    else:
        flash("File artifact not found on local disk storage.", "danger")
        return redirect(url_for('cloud_files'))

@app.route('/cloud-files/delete/<int:file_id>', methods=['POST'])
@login_required_custom
def delete_cloud_file(file_id):
    f = CloudFile.query.get_or_404(file_id)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(f)
    db.session.commit()
    flash("File deleted from cloud storage.", "info")
    return redirect(url_for('cloud_files'))

# ==========================================
# 3. 🧠 STUDENT PERFORMANCE PREDICTION USING AI
# ==========================================

@app.route('/student-prediction', methods=['GET', 'POST'])
@login_required_custom
def student_prediction():
    prediction_result = None
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        roll_no = request.form.get('roll_no')
        attendance = float(request.form.get('attendance', 80))
        internal1 = float(request.form.get('internal1', 75))
        internal2 = float(request.form.get('internal2', 78))
        assignment = float(request.form.get('assignment', 85))
        study_hours = float(request.form.get('study_hours', 3))
        
        ai_res = predict_student_performance(attendance, internal1, internal2, assignment, study_hours)
        
        pred_record = StudentPrediction(
            student_name=student_name, roll_no=roll_no,
            attendance_pct=attendance, internal1_mark=internal1, internal2_mark=internal2,
            assignment_score=assignment, study_hours_per_day=study_hours,
            predicted_grade=ai_res['predicted_grade'], predicted_gpa=ai_res['predicted_gpa'],
            risk_level=ai_res['risk_level'], ai_recommendations=ai_res['recommendations']
        )
        db.session.add(pred_record)
        db.session.commit()
        prediction_result = {**ai_res, 'student_name': student_name, 'roll_no': roll_no}
        flash("AI Performance Diagnostic complete!", "success")
        
    history = StudentPrediction.query.order_by(StudentPrediction.created_at.desc()).limit(10).all()
    return render_template('modules/student_prediction.html', result=prediction_result, history=history)

# ==========================================
# 4. 🚌 BUS TRACKING SYSTEM
# ==========================================

@app.route('/bus-tracking')
@login_required_custom
def bus_tracking():
    routes = BusRoute.query.all()
    for route in routes:
        if route.stops_json:
            try:
                route.parsed_stops = json.loads(route.stops_json)
            except:
                route.parsed_stops = []
        else:
            route.parsed_stops = []
    return render_template('modules/bus_tracking.html', routes=routes)

@app.route('/api/bus/<int:id>/update-location', methods=['POST'])
@login_required_custom
def update_bus_location(id):
    route = BusRoute.query.get_or_404(id)
    data = request.get_json() or {}
    if 'current_stop' in data: route.current_stop = data['current_stop']
    if 'next_stop' in data: route.next_stop = data['next_stop']
    if 'eta_minutes' in data: route.eta_minutes = int(data['eta_minutes'])
    if 'speed_kmph' in data: route.speed_kmph = float(data['speed_kmph'])
    if 'status' in data: route.status = data['status']
    db.session.commit()
    return jsonify({"success": True, "message": "Live GPS telemetry updated"})

# ==========================================
# 5. 📰 HEADLINE IN INDIA
# ==========================================

@app.route('/headlines', methods=['GET', 'POST'])
@login_required_custom
def headlines():
    category_filter = request.args.get('category', 'All')
    if category_filter != 'All':
        news_items = IndianHeadline.query.filter_by(category=category_filter).order_by(IndianHeadline.published_at.desc()).all()
    else:
        news_items = IndianHeadline.query.order_by(IndianHeadline.published_at.desc()).all()
        
    trending_news = IndianHeadline.query.filter_by(is_trending=True).limit(4).all()
    return render_template('modules/headlines.html', news=news_items, trending=trending_news, current_cat=category_filter)

@app.route('/headlines/add', methods=['POST'])
@login_required_custom
def add_headline():
    title = request.form.get('title')
    category = request.form.get('category')
    source = request.form.get('source')
    summary = request.form.get('summary')
    is_trending = bool(request.form.get('is_trending'))
    
    new_h = IndianHeadline(
        title=title, category=category, source=source,
        summary=summary, is_trending=is_trending
    )
    db.session.add(new_h)
    db.session.commit()
    flash("News flash published to Indian News Feed!", "success")
    return redirect(url_for('headlines'))

# ==========================================
# 6. 🏆 E-COMMERCE FOR SPORTS PRODUCTS
# ==========================================

@app.route('/sports-ecom')
@login_required_custom
def sports_ecom():
    cat = request.args.get('cat', 'All')
    if cat != 'All':
        products = SportsProduct.query.filter_by(category=cat).all()
    else:
        products = SportsProduct.query.all()
    orders = SportsOrder.query.order_by(SportsOrder.created_at.desc()).limit(5).all()
    return render_template('modules/sports_ecom.html', products=products, current_cat=cat, orders=orders)

@app.route('/sports-ecom/add', methods=['POST'])
@login_required_custom
def add_sports_product():
    name = request.form.get('name')
    category = request.form.get('category')
    brand = request.form.get('brand', 'VVK Pro Sports')
    price = float(request.form.get('price', 999.0))
    original_price = float(request.form.get('original_price', price * 1.3))
    stock_count = int(request.form.get('stock_count', 20))
    description = request.form.get('description', '')
    image_url = request.form.get('image_url') or 'https://images.unsplash.com/photo-1517649763962-0c623266ddc0?auto=format&fit=crop&w=400&q=80'
    
    new_product = SportsProduct(
        name=name, category=category, brand=brand,
        price=price, original_price=original_price,
        stock_count=stock_count, description=description,
        image_url=image_url, rating=4.8
    )
    db.session.add(new_product)
    db.session.commit()
    flash(f"New product '{name}' added to sports inventory catalogue!", "success")
    return redirect(url_for('sports_ecom'))

@app.route('/api/sports/order', methods=['POST'])
@login_required_custom
def create_sports_order():
    data = request.get_json()
    order_num = f"VVK-SPORTS-{uuid.uuid4().hex[:6].upper()}"
    new_order = SportsOrder(
        order_id=order_num,
        customer_name=data.get('customer_name', 'Student Customer'),
        phone=data.get('phone', '+91 98000 00000'),
        items_json=json.dumps(data.get('items', [])),
        total_amount=float(data.get('total_amount', 0)),
        payment_method=data.get('payment_method', 'UPI / GPay'),
        status='Order Placed & Confirmed'
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"success": True, "order_id": order_num, "message": "Order successfully booked!"})

# ==========================================
# 7. 💻 AI CODE REVIEWER & BUG FIXER
# ==========================================

@app.route('/ai-code-reviewer', methods=['GET', 'POST'])
@login_required_custom
def ai_code_reviewer():
    review_output = None
    input_code = ""
    language = "python"
    
    if request.method == 'POST':
        language = request.form.get('language', 'python')
        input_code = request.form.get('code', '')
        
        ai_res = analyze_code_with_ai(input_code, language)
        
        session_rec = CodeReviewSession(
            language=language,
            submitted_code=input_code,
            bugs_detected=json.dumps(ai_res['bugs']),
            security_issues=json.dumps(ai_res['security']),
            fixed_code=ai_res['fixed_code'],
            optimization_score=ai_res['optimization_score'],
            complexity=ai_res['complexity']
        )
        db.session.add(session_rec)
        db.session.commit()
        review_output = ai_res
        flash("AI Static & Dynamic Code Inspection completed!", "success")
        
    recent_reviews = CodeReviewSession.query.order_by(CodeReviewSession.created_at.desc()).limit(5).all()
    return render_template('modules/ai_code_reviewer.html', output=review_output, input_code=input_code, lang=language, recent=recent_reviews)

# ==========================================
# 8. 📝 STUDENT ASSESSMENT USING AI
# ==========================================

@app.route('/student-assessment', methods=['GET', 'POST'])
@login_required_custom
def student_assessment():
    assessment_history = StudentAssessment.query.order_by(StudentAssessment.created_at.desc()).all()
    return render_template('modules/student_assessment.html', history=assessment_history)

@app.route('/api/assessment/submit', methods=['POST'])
@login_required_custom
def submit_assessment():
    data = request.get_json()
    student_name = data.get('student_name', 'Student Candidate')
    roll_no = data.get('roll_no', 'VVK23001')
    subject = data.get('subject', 'AI & Data Structures')
    correct = int(data.get('correct_answers', 0))
    total = int(data.get('total_questions', 10))
    time_taken = int(data.get('time_taken', 120))
    
    score_pct = round((correct / total) * 100.0, 1)
    
    # Gemini AI Evaluation
    gemini_eval = evaluate_assessment_with_gemini(student_name, subject, score_pct, correct, total)
    strengths = gemini_eval.get('strengths', 'Solid core reasoning.')
    improvements = gemini_eval.get('improvements', 'Practice complex scenarios.')
    feedback = gemini_eval.get('feedback', 'Keep learning!')

    assessment = StudentAssessment(
        student_name=student_name, roll_no=roll_no, subject=subject,
        score=score_pct, total_questions=total, correct_answers=correct,
        time_taken_seconds=time_taken, strength_areas=strengths,
        improvement_areas=improvements, ai_feedback=feedback
    )
    db.session.add(assessment)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "score_pct": score_pct,
        "strengths": strengths,
        "improvements": improvements,
        "feedback": feedback
    })

# ==========================================
# 9. 📈 CUSTOMER RELATIONSHIP MANAGEMENT (CRM)
# ==========================================

@app.route('/crm', methods=['GET', 'POST'])
@login_required_custom
def crm():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        contact_person = request.form.get('contact_person')
        email = request.form.get('email')
        phone = request.form.get('phone')
        deal_value = float(request.form.get('deal_value', 100000))
        stage = request.form.get('stage', 'Lead')
        lead_source = request.form.get('lead_source', 'Campus Outreach')
        assigned_to = request.form.get('assigned_to', 'Placement & Industry Cell')
        notes = request.form.get('notes', '')
        
        lead = CRMLead(
            company_name=company_name, contact_person=contact_person, email=email,
            phone=phone, deal_value=deal_value, stage=stage, lead_source=lead_source,
            assigned_to=assigned_to, notes=notes
        )
        db.session.add(lead)
        db.session.commit()
        flash("Corporate Partner / Recruiter Lead logged into CRM pipeline!", "success")
        return redirect(url_for('crm'))
        
    leads = CRMLead.query.order_by(CRMLead.created_at.desc()).all()
    total_pipeline = sum(l.deal_value for l in leads)
    stage_counts = {
        'Lead': CRMLead.query.filter_by(stage='Lead').count(),
        'Contacted': CRMLead.query.filter_by(stage='Contacted').count(),
        'Proposal': CRMLead.query.filter_by(stage='Proposal').count(),
        'Won': CRMLead.query.filter_by(stage='Won').count()
    }
    return render_template('modules/crm.html', leads=leads, total_pipeline=total_pipeline, stages=stage_counts)

@app.route('/api/crm/<int:id>/update-stage', methods=['POST'])
@login_required_custom
def update_crm_stage(id):
    lead = CRMLead.query.get_or_404(id)
    data = request.get_json() or {}
    lead.stage = data.get('stage', lead.stage)
    db.session.commit()
    return jsonify({"success": True, "message": "Pipeline stage updated!"})

# ==========================================
# 10. 🕵️ FAKE NEWS DETECTION & REPORTING
# ==========================================

@app.route('/fakenews', methods=['GET', 'POST'])
@login_required_custom
def fakenews():
    result = None
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        source_url = request.form.get('source_url', '')
        
        ai_res = detect_fake_news_ai(title, content, source_url)
        
        report = FakeNewsReport(
            news_title=title, news_content=content, source_url=source_url,
            credibility_score=ai_res['credibility_score'],
            prediction=ai_res['prediction'],
            linguistic_cues=ai_res['linguistic_cues'],
            reported_by=session.get('user', 'user')
        )
        db.session.add(report)
        db.session.commit()
        result = ai_res
        flash("AI Credibility Analysis completed!", "success")
        
    reports = FakeNewsReport.query.order_by(FakeNewsReport.created_at.desc()).limit(8).all()
    return render_template('modules/fakenews.html', result=result, reports=reports)

# ==========================================
# 11. 🪙 GOLD & SILVER FAKE / PURITY DETECTION
# ==========================================

@app.route('/gold-silver', methods=['GET', 'POST'])
@login_required_custom
def gold_silver():
    test_result = None
    if request.method == 'POST':
        metal_type = request.form.get('metal_type', 'Gold')
        weight_air = float(request.form.get('weight_air', 10.0))
        weight_water = float(request.form.get('weight_water', 9.48))
        hallmark = request.form.get('hallmark', '')
        acid_test = request.form.get('acid_test', 'No Reaction (Pass)')
        magnet_test = request.form.get('magnet_test', 'Non-Magnetic (Pass)')
        
        calc = calculate_metal_purity(metal_type, weight_air, weight_water, hallmark)
        
        record = MetalPurityTest(
            metal_type=metal_type, weight_in_air_g=weight_air,
            weight_in_water_g=weight_water, calculated_density=calc['density'],
            hallmark_number=hallmark, acid_test_result=acid_test,
            magnet_test=magnet_test, estimated_karat=calc['estimated_karat'],
            purity_percentage=calc['purity_percentage'],
            verdict=calc['verdict']
        )
        db.session.add(record)
        db.session.commit()
        test_result = {**calc, 'weight_air': weight_air, 'metal_type': metal_type}
        flash("Hydrostatic & Metallurgical purity verification calculated!", "success")
        
    history = MetalPurityTest.query.order_by(MetalPurityTest.created_at.desc()).limit(8).all()
    return render_template('modules/gold_silver.html', result=test_result, history=history)

# ==========================================
# 12. 🏏 CRICKET CLUB MANAGEMENT SYSTEM
# ==========================================

@app.route('/cricket-club', methods=['GET', 'POST'])
@login_required_custom
def cricket_club():
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        style = request.form.get('batting_style', 'Right Hand')
        matches = int(request.form.get('matches', 0))
        runs = int(request.form.get('runs', 0))
        wickets = int(request.form.get('wickets', 0))
        
        avg = round(runs / max(1, matches), 1)
        sr = 125.0
        
        new_player = CricketPlayer(
            name=name, role=role, batting_style=style,
            matches_played=matches, runs_scored=runs,
            wickets_taken=wickets, batting_avg=avg, strike_rate=sr
        )
        db.session.add(new_player)
        db.session.commit()
        flash(f"Player {name} added to Vivekanandha Cricket Squad roster!", "success")
        return redirect(url_for('cricket_club'))
        
    players = CricketPlayer.query.all()
    matches = CricketMatch.query.order_by(CricketMatch.id.desc()).all()
    return render_template('modules/cricket_club.html', players=players, matches=matches)

# ==========================================
# 13. 🏍️ TWO-WHEELER SERVICE & MAINTENANCE
# ==========================================

@app.route('/two-wheeler', methods=['GET', 'POST'])
@login_required_custom
def two_wheeler():
    if request.method == 'POST':
        name = request.form.get('customer_name')
        phone = request.form.get('phone_number')
        bike_model = request.form.get('bike_model')
        vehicle_num = request.form.get('vehicle_number')
        service_type = request.form.get('service_type')
        issues = request.form.get('issues_reported')
        cost = float(request.form.get('estimated_cost', 1200.0))
        
        service_booking = TwoWheelerService(
            customer_name=name, phone_number=phone,
            bike_model=bike_model, vehicle_number=vehicle_num,
            service_type=service_type, issues_reported=issues,
            estimated_cost=cost, service_status='Vehicle Received'
        )
        db.session.add(service_booking)
        db.session.commit()
        flash(f"Service slot booked for vehicle {vehicle_num}!", "success")
        return redirect(url_for('two_wheeler'))
        
    services = TwoWheelerService.query.order_by(TwoWheelerService.booking_date.desc()).all()
    return render_template('modules/two_wheeler.html', services=services)

@app.route('/api/two-wheeler/<int:id>/status', methods=['POST'])
@login_required_custom
def update_two_wheeler_status(id):
    svc = TwoWheelerService.query.get_or_404(id)
    data = request.get_json() or {}
    svc.service_status = data.get('service_status', svc.service_status)
    db.session.commit()
    return jsonify({"success": True, "message": "Bike service lifecycle updated!"})

# ==========================================
# 14. 🎓 INTERCOLLEGIATE REGISTRATION MANAGEMENT
# ==========================================

@app.route('/intercollege', methods=['GET', 'POST'])
@login_required_custom
def intercollege():
    if request.method == 'POST':
        ticket = f"VVK-SYMP-{uuid.uuid4().hex[:5].upper()}"
        name = request.form.get('participant_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        college = request.form.get('college_name')
        dept = request.form.get('department')
        event = request.form.get('event_category')
        team_size = int(request.form.get('team_size', 1))
        team_members = request.form.get('team_members', '')
        
        registration = IntercollegeRegistration(
            ticket_id=ticket, participant_name=name, email=email, phone=phone,
            college_name=college, department=dept, event_category=event,
            team_size=team_size, team_members=team_members,
            payment_status=f"Confirmed (Badge: {ticket})"
        )
        db.session.add(registration)
        db.session.commit()
        flash(f"Registration successful! Your official Pass ID is {ticket}", "success")
        return redirect(url_for('intercollege'))
        
    registrations = IntercollegeRegistration.query.order_by(IntercollegeRegistration.created_at.desc()).all()
    return render_template('modules/intercollege.html', registrations=registrations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
