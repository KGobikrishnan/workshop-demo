import json
from models import (
    db, User, Complaint, CloudFile, StudentPrediction, BusRoute, IndianHeadline,
    SportsProduct, SportsOrder, CodeReviewSession, StudentAssessment, CRMLead,
    FakeNewsReport, MetalPurityTest, CricketPlayer, CricketMatch, TwoWheelerService,
    IntercollegeRegistration
)
from werkzeug.security import generate_password_hash

def seed_database():
    # 1. Seed default user if not exists
    if not User.query.filter_by(username='user').first():
        default_user = User(
            username='user',
            password=generate_password_hash('1234'),
            role='student'
        )
        db.session.add(default_user)

    # 2. Seed Complaints
    if Complaint.query.count() == 0:
        c1 = Complaint(
            student_name="Praveen Kumar", reg_number="VVK22CS104", department="Computer Science & Engineering",
            category="Lab", title="GPU Server CUDA Drivers not responding in AI Lab 3",
            description="The PyTorch acceleration node in AI Lab 3 is experiencing driver mismatch errors during deep learning practicals.",
            priority="High", status="In-Progress", admin_remark="Lab technician assigned for driver reinstall."
        )
        c2 = Complaint(
            student_name="Ananya Sri", reg_number="VVK23IT045", department="Information Technology",
            category="Hostel", title="Wi-Fi Router 5GHz connectivity drops in Ganga Block 3rd floor",
            description="Frequent packet drops during evening study hours in rooms 301 to 312.",
            priority="Medium", status="Open", admin_remark="Network team notified."
        )
        c3 = Complaint(
            student_name="Karthik Raja", reg_number="VVK21ME088", department="Mechanical Engineering",
            category="Transport", title="Bus No. 12 Route AC cooling maintenance required",
            description="AC blower is making rattling noise on Salem express route.",
            priority="Low", status="Resolved", admin_remark="Blower bearing replaced and tested."
        )
        db.session.add_all([c1, c2, c3])

    # 3. Seed Cloud Files
    if CloudFile.query.count() == 0:
        f1 = CloudFile(
            filename="VVK_Deep_Learning_Unit_1_4.pdf", original_name="Deep_Learning_Lecture_Notes.pdf",
            file_type="PDF Document", file_size_kb=4250.0, category="Notes", uploaded_by="Dr. S. Ramanathan"
        )
        f2 = CloudFile(
            filename="FullStack_Project_Guidelines_2026.docx", original_name="Project_Guidelines_2026.docx",
            file_type="Word Document", file_size_kb=1120.5, category="Assignment", uploaded_by="Prof. M. Malathi"
        )
        f3 = CloudFile(
            filename="Vivekanandha_Campus_Hackathon_Rules.pdf", original_name="Campus_Hackathon_Schedule.pdf",
            file_type="PDF Document", file_size_kb=890.0, category="Circular", uploaded_by="admin"
        )
        db.session.add_all([f1, f2, f3])

    # 4. Seed Bus Routes
    if BusRoute.query.count() == 0:
        b1 = BusRoute(
            bus_number="VVK-BUS-01", route_name="Salem New Bus Stand -> VVK Main Campus",
            driver_name="M. Selvam", driver_phone="+91 98421 11234",
            current_stop="Seelanaickenpatti Junction", next_stop="Rasipuram Bypass",
            eta_minutes=18, speed_kmph=52.0, status="On-Time", capacity_pct=78,
            stops_json=json.dumps(["Salem New Bus Stand", "Kondalampatti", "Seelanaickenpatti", "Rasipuram Bypass", "Elampillai Turn", "VVK Central Gate"])
        )
        b2 = BusRoute(
            bus_number="VVK-BUS-04", route_name="Erode Collectorate -> Tiruchengode VVK Campus",
            driver_name="R. Ganesan", driver_phone="+91 94432 55678",
            current_stop="Pallipalayam Bridge", next_stop="Komarapalayam Ring Road",
            eta_minutes=12, speed_kmph=46.5, status="On-Time", capacity_pct=60,
            stops_json=json.dumps(["Erode Collectorate", "Bhavani Junction", "Pallipalayam Bridge", "Komarapalayam", "VVK South Gate"])
        )
        b3 = BusRoute(
            bus_number="VVK-BUS-08", route_name="Namakkal Bus Stand -> VVK Campus",
            driver_name="S. Chinnasamy", driver_phone="+91 97890 99881",
            current_stop="Velur Road Signal", next_stop="Tiruchengode Toll",
            eta_minutes=25, speed_kmph=48.0, status="Delayed (Traffic)", capacity_pct=85,
            stops_json=json.dumps(["Namakkal Bus Stand", "Thuraiyur Pirivu", "Velur Road", "Tiruchengode Toll", "VVK North Gate"])
        )
        db.session.add_all([b1, b2, b3])

    # 5. Seed Indian Headlines
    if IndianHeadline.query.count() == 0:
        h1 = IndianHeadline(
            title="India's Semiconductor Mission: 4 New Fab & Packaging Units Begin Construction",
            category="Technology", source="TechBharat News",
            summary="The semiconductor ecosystem in India expands significantly with advanced silicon wafer fabrication facilities in Gujarat and Tamil Nadu receiving expedited approvals.",
            read_time="3 min read", is_trending=True
        )
        h2 = IndianHeadline(
            title="AI and Quantum Computing Curriculum Mandated Across Autonomous Engineering Colleges",
            category="Higher Education", source="National Education Express",
            summary="UGC and AICTE announce unified experiential computing guidelines to prepare 2026 engineering graduates for frontier AI tooling and generative system design.",
            read_time="4 min read", is_trending=True
        )
        h3 = IndianHeadline(
            title="Team India Unveils High-Performance Squad for Upcoming T20 World Championship",
            category="Sports", source="CricBharat Sports",
            summary="Dynamic youth talent from inter-collegiate and domestic leagues make headlines as national selectors announce the 15-player powerhouse squad.",
            read_time="2 min read", is_trending=False
        )
        h4 = IndianHeadline(
            title="Tamil Nadu Clean Energy Grid crosses 55% Renewable Generation Milestone",
            category="National", source="The Deccan Monitor",
            summary="Massive offshore wind turbines and rooftop solar adoption push southern state power grids into net-positive renewable energy generation.",
            read_time="3 min read", is_trending=False
        )
        db.session.add_all([h1, h2, h3, h4])

    # 6. Seed Sports Products
    if SportsProduct.query.count() == 0:
        p1 = SportsProduct(
            name="SS Kashmir Willow Pro Grade-1 Cricket Bat", category="Cricket",
            price=2499.0, original_price=3999.0, rating=4.8, stock_count=18,
            description="Handcrafted premium willow bat with massive sweet spot, thick edges, and balanced pickup for tournament play.",
            image_url="https://images.unsplash.com/photo-1593341646782-e0b495cffd6d?auto=format&fit=crop&w=400&q=80",
            brand="SS Sunridges"
        )
        p2 = SportsProduct(
            name="Yonex Nanoray Carbon Fiber Badminton Racket Set (Pack of 2)", category="Badminton",
            price=1850.0, original_price=2799.0, rating=4.7, stock_count=24,
            description="Ultra-lightweight aerodynamic frame with high-tension BG-65 strings and full thermal cover.",
            image_url="https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=400&q=80",
            brand="Yonex"
        )
        p3 = SportsProduct(
            name="Nivia Storm Football (FIFA Pro Approved Size 5)", category="Football",
            price=799.0, original_price=1299.0, rating=4.6, stock_count=40,
            description="32-panel thermal bonded rubber construction offering pinpoint trajectory and zero water absorption.",
            image_url="https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=400&q=80",
            brand="Nivia"
        )
        p4 = SportsProduct(
            name="Kore 20Kg Hexa Dumbbell & Home Gym Fitness Kit", category="Gym & Fitness",
            price=1699.0, original_price=2999.0, rating=4.5, stock_count=15,
            description="Anti-roll rubber coated solid weights with chrome knurled bar and protective floor grips.",
            image_url="https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=400&q=80",
            brand="Kore Fitness"
        )
        db.session.add_all([p1, p2, p3, p4])

    # 7. Seed CRM Leads
    if CRMLead.query.count() == 0:
        l1 = CRMLead(
            company_name="Cognizant Digital Engineering", contact_person="V. Sundarraj",
            email="sundarraj.v@cognizant.com", phone="+91 94441 23098", deal_value=450000.0,
            stage="Proposal", lead_source="Annual Placement Drive", assigned_to="Dean Placement",
            notes="Exclusive pool campus drive scheduled for 250+ CSE & IT candidates."
        )
        l2 = CRMLead(
            company_name="L&T Infotech Solutions", contact_person="Meenakshi Sundaram",
            email="m.sundaram@lntinfotech.com", phone="+91 98840 88712", deal_value=320000.0,
            stage="Negotiation", lead_source="Industry MoU Partnership", assigned_to="R&D Cell",
            notes="Setting up Centre of Excellence (CoE) in Embedded IoT & Robotics."
        )
        l3 = CRMLead(
            company_name="Zoho Corporation Pvt Ltd", contact_person="Aravind Balaji",
            email="aravind.b@zohocorp.com", phone="+91 99620 44102", deal_value=600000.0,
            stage="Won", lead_source="Hackathon Sponsorship", assigned_to="Corporate Relations",
            notes="Title sponsorship confirmed for National TechSymposium 2026."
        )
        db.session.add_all([l1, l2, l3])

    # 8. Seed Cricket Club Players & Matches
    if CricketPlayer.query.count() == 0:
        p1 = CricketPlayer(name="R. Dinesh (C)", role="All-Rounder", batting_style="Right Hand / Off-Break", matches_played=18, runs_scored=540, wickets_taken=24, batting_avg=45.0, strike_rate=142.0)
        p2 = CricketPlayer(name="S. Vignesh", role="Batsman", batting_style="Right Hand Opener", matches_played=16, runs_scored=610, wickets_taken=0, batting_avg=48.5, strike_rate=136.8)
        p3 = CricketPlayer(name="M. Ashwin", role="Bowler", batting_style="Left Arm Fast", matches_played=14, runs_scored=85, wickets_taken=29, batting_avg=14.1, strike_rate=98.0)
        p4 = CricketPlayer(name="G. Praveen (WK)", role="Wicket Keeper", batting_style="Right Hand Middle Order", matches_played=15, runs_scored=390, wickets_taken=0, batting_avg=39.0, strike_rate=125.4)
        db.session.add_all([p1, p2, p3, p4])

    if CricketMatch.query.count() == 0:
        m1 = CricketMatch(
            match_title="Anna University Zonal T20 Trophy - Quarter Final",
            team1="Vivekanandha Warriors", team2="Kongu Kings XI",
            venue="VVK Central Stadium", match_date="2026-08-22 09:30 AM",
            status="Upcoming", score_team1="-", score_team2="-", result="Starts in 4 Days"
        )
        m2 = CricketMatch(
            match_title="District Inter-College Championship",
            team1="Vivekanandha Warriors", team2="KSR Strikers",
            venue="Salem Municipal Ground", match_date="2026-08-14 02:00 PM",
            status="Completed", score_team1="184/5 (20.0)", score_team2="152/9 (20.0)",
            result="Vivekanandha Warriors won by 32 runs (Player of the Match: R. Dinesh)"
        )
        db.session.add_all([m1, m2])

    # 9. Seed Two Wheeler Services
    if TwoWheelerService.query.count() == 0:
        s1 = TwoWheelerService(
            customer_name="Vijay Anand", phone_number="+91 98401 22334",
            bike_model="Yamaha MT-15 V2", vehicle_number="TN-34-BX-4450",
            service_type="General Service + Synthetic Oil Change",
            issues_reported="Chain slackness, front disc brake squeak, air filter cleanup required.",
            estimated_cost=1450.0, service_status="Ready for Delivery",
            mechanic_assigned="Senior Tech Rajendran"
        )
        s2 = TwoWheelerService(
            customer_name="Deepak Raj", phone_number="+91 97892 44556",
            bike_model="Royal Enfield Classic 350", vehicle_number="TN-28-AQ-8890",
            service_type="Full Overhaul & Tappet Setting",
            issues_reported="Clutch cable hard, engine heating in bumper-to-bumper traffic.",
            estimated_cost=2800.0, service_status="In-Progress",
            mechanic_assigned="Master Tech S. Kumar"
        )
        db.session.add_all([s1, s2])

    # 10. Seed Intercollege Registrations
    if IntercollegeRegistration.query.count() == 0:
        r1 = IntercollegeRegistration(
            ticket_id="VVK-TECH-9012", participant_name="Harish Kumar & Team",
            email="harish.k@psgtech.edu", phone="+91 98430 77123",
            college_name="PSG College of Technology, Coimbatore", department="Information Technology",
            event_category="24h AI Generative Hackathon", team_size=4,
            team_members="Harish K (Lead), Swetha R, Gokul V, Preethi M",
            payment_status="Confirmed (Ticket ID: VVK-TECH-9012)"
        )
        r2 = IntercollegeRegistration(
            ticket_id="VVK-CODE-4419", participant_name="Sandhiya Mohan",
            email="sandhiya.m@gct.ac.in", phone="+91 97512 88990",
            college_name="Government College of Technology (GCT), Coimbatore", department="Computer Science & Engineering",
            event_category="Speed Debugging & Algorithmic Sprint", team_size=1,
            team_members="Sandhiya Mohan",
            payment_status="Confirmed (Ticket ID: VVK-CODE-4419)"
        )
        db.session.add_all([r1, r2])

    db.session.commit()
    print("Database seeding completed successfully!")
