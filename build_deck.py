"""
build_deck.py
Generates the professional MoveInSync FDE Case Study Presentation Deck (.pptx)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Palette
    NAVY = RGBColor(15, 23, 42)       # #0f172a
    DARK_BLUE = RGBColor(30, 41, 59)   # #1e293b
    CARD_BG = RGBColor(248, 250, 252)  # #f8fafc
    CARD_BORDER = RGBColor(226, 232, 240)
    PRIMARY = RGBColor(37, 99, 235)    # #2563eb
    ACCENT_GOLD = RGBColor(245, 158, 11) # #f59e0b
    TEXT_MAIN = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139)
    WHITE = RGBColor(255, 255, 255)
    RED = RGBColor(239, 68, 68)
    GREEN = RGBColor(16, 185, 129)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title, subtitle):
        # Header text
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 1: COVER
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    # Title box
    tbox = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "MOVEINSYNC EMPLOYEE APP"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Play Store Ratings Diagnosis & Turnaround Strategy"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "Forward Deployed Engineer (FDE) Case Study Solution & Execution Roadmap"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # Metadata cards on cover
    metrics = [
        ("4.32", "Lifetime Rating (114.5k reviews)"),
        ("~3.0", "Recent 30-Day Average"),
        ("12%", "1-Star Rating Share"),
        ("60 Days", "Target Recovery to 4.3+ Stars")
    ]
    card_w = Inches(2.6)
    gap = Inches(0.3)
    start_x = Inches(1.0)
    for i, (val, label) in enumerate(metrics):
        cx = start_x + i * (card_w + gap)
        cshape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(5.2), card_w, Inches(1.3))
        cshape.fill.solid()
        cshape.fill.fore_color.rgb = DARK_BLUE
        cshape.line.color.rgb = RGBColor(51, 65, 85)
        
        ctf = cshape.text_frame
        ctf.word_wrap = True
        ctf.margin_top = Inches(0.18)
        cp1 = ctf.paragraphs[0]
        cp1.alignment = PP_ALIGN.CENTER
        cp1.text = val
        cp1.font.size = Pt(26)
        cp1.font.bold = True
        cp1.font.color.rgb = ACCENT_GOLD if i in [0, 3] else (RED if i == 2 else WHITE)
        
        cp2 = ctf.add_paragraph()
        cp2.alignment = PP_ALIGN.CENTER
        cp2.text = label
        cp2.font.size = Pt(10)
        cp2.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # SLIDE 2: THE CORE DILEMMA & PROBLEM ANATOMY
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "The Core Dilemma: The Silent Rating Erosion", 
               "Why a 4.32 star vanity metric masks a high-severity customer satisfaction cliff")

    # Left Column: The Trap
    left_card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    ltf = left_card.text_frame
    ltf.margin_left = Inches(0.3); ltf.margin_top = Inches(0.3); ltf.margin_right = Inches(0.3)
    
    lp = ltf.paragraphs[0]
    lp.text = "The Mathematical Inertia Trap"
    lp.font.size = Pt(18); lp.font.bold = True; lp.font.color.rgb = NAVY; lp.space_after = Pt(10)
    
    bullets_l = [
        ("Massive Lifetime Base:", " 114,500+ lifetime reviews anchor the public store badge at 4.32, creating a false sense of health."),
        ("Recent Rolling Average:", " New reviews over the last 30 days average ~3.0 stars, indicating recent release regression."),
        ("U-Shaped Bimodal Curve:", " Ratings are split between 5-star happy commuters and 1-star furious employees hit by operational penalties."),
        ("B2B2C Vulnerability:", " Enterprise employees cannot switch apps; when frustrated, the public Google Play Store is their only escalation forum.")
    ]
    for b_title, b_desc in bullets_l:
        bp = ltf.add_paragraph()
        bp.space_after = Pt(10)
        run1 = bp.add_run(); run1.text = "• " + b_title; run1.font.bold = True; run1.font.size = Pt(12); run1.font.color.rgb = PRIMARY
        run2 = bp.add_run(); run2.text = b_desc; run2.font.size = Pt(12); run2.font.color.rgb = TEXT_MAIN

    # Right Column: Distribution & Breakdown
    right_card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = CARD_BORDER
    rtf = right_card.text_frame
    rtf.margin_left = Inches(0.3); rtf.margin_top = Inches(0.3); rtf.margin_right = Inches(0.3)

    rp = rtf.paragraphs[0]
    rp.text = "Rating Distribution & Negative Sentiment Mix"
    rp.font.size = Pt(18); rp.font.bold = True; rp.font.color.rgb = NAVY; rp.space_after = Pt(10)

    dist_items = [
        ("★★★★★ (5 Stars)", "68%", GREEN),
        ("★★★★☆ (4 Stars)", "12%", GREEN),
        ("★★★☆☆ (3 Stars)", "4%", ACCENT_GOLD),
        ("★★☆☆☆ (2 Stars)", "4%", ACCENT_GOLD),
        ("★☆☆☆☆ (1 Star)", "12% (~13,700 users)", RED)
    ]
    for star_lbl, pct_val, clr in dist_items:
        dp = rtf.add_paragraph()
        dp.space_after = Pt(6)
        r = dp.add_run(); r.text = f"{star_lbl} : {pct_val}"; r.font.bold = True; r.font.size = Pt(12); r.font.color.rgb = clr

    rp_sep = rtf.add_paragraph()
    rp_sep.text = "Primary Complaint Drivers (from 1-Star Analysis):"
    rp_sep.font.bold = True; rp_sep.font.size = Pt(13); rp_sep.font.color.rgb = NAVY; rp_sep.space_before = Pt(8); rp_sep.space_after = Pt(6)

    complaints = [
        "1. Driver No-Show penalties & false salary deductions (45% of 1★)",
        "2. Booking date jump bug / incorrect date allocation (25% of 1★)",
        "3. Live GPS lag & erratic ETA jumps (15% of 1★)",
        "4. UI confusion, background crashes & 0% dev reply rate (15% of 1★)"
    ]
    for c in complaints:
        cp = rtf.add_paragraph()
        cp.text = "• " + c
        cp.font.size = Pt(11); cp.font.color.rgb = TEXT_MAIN; cp.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 3: ROOT CAUSE ANALYSIS (5 CRITICAL FAILURE MODES)
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Root Cause Analysis: Why Users Are Angry", 
               "Systemic classification across Product, Engineering, and Field Operations")

    causes = [
        ("P0-1: Driver No-Show & Penalty Deduction", "FINANCIAL IMPACT", RED,
         "Driver prematurely marks 'No Show' while employee is waiting at pickup spot. Automatic payroll penalties trigger without employee verification or GPS proximity fence check."),
        ("P0-2: Date Picker & Booking Time Glitch", "CORE WORKFLOW BREAK", RED,
         "Booking calendar defaults to current day instead of next workday, causing accidental bookings, lost seat allocations, and employee disciplinary strikes."),
        ("P0-3: GPS Telemetry & Phantom Pickup Times", "TECH STACK / INFRA", RED,
         "Driver location freezes or updates every 3-5 mins due to aggressive OS background battery killers on cheap driver handsets. ETA jumps erratically."),
        ("P0-4: Developer Zero-Reply Deficit", "COMMUNITY TRUST", ACCENT_GOLD,
         "Public Play Store response rate is near 0%. Disgruntled enterprise users feel completely unheard, amplifying negative review retention."),
        ("P0-5: Android 14/15 Background Crash Spikes", "STABILITY & CRASH", ACCENT_GOLD,
         "Strict background battery optimization kills Foreground Location Services, crashing the app at launch on newer OEM ROMs.")
    ]

    card_h = Inches(1.0)
    gap_y = Inches(0.12)
    start_y = Inches(1.5)
    for i, (title, tag, tag_clr, desc) in enumerate(causes):
        y = start_y + i * (card_h + gap_y)
        c = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), card_h)
        c.fill.solid(); c.fill.fore_color.rgb = CARD_BG; c.line.color.rgb = CARD_BORDER
        ctf = c.text_frame
        ctf.margin_left = Inches(0.25); ctf.margin_top = Inches(0.15); ctf.margin_right = Inches(0.25)
        
        p = ctf.paragraphs[0]
        r1 = p.add_run(); r1.text = title; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = NAVY
        r_tag = p.add_run(); r_tag.text = f"  [{tag}]"; r_tag.font.bold = True; r_tag.font.size = Pt(10); r_tag.font.color.rgb = tag_clr
        
        p2 = ctf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11); p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 4: PRIORITY ACTION PLAN MATRIX
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "FDE Action Plan: Targeted Solutions & Ownership", 
               "High-leverage engineering & operational interventions prioritized by impact")

    # Table
    rows = 6; cols = 5
    tbl_shape = slide4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    table = tbl_shape.table
    table.columns[0].width = Inches(1.1)
    table.columns[1].width = Inches(2.5)
    table.columns[2].width = Inches(4.3)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(2.0)

    headers = ["Priority", "Problem Area", "Engineering & Operational Intervention", "Owner", "Target Metric"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = WHITE

    data = [
        ("P0", "No-Show & Penalty", "Enforce 50m Geofence + 3-min countdown before driver can hit No-Show; 24h grace dispute window", "FDE + Backend Eng", "-70% No-show disputes"),
        ("P0", "Booking Date Bug", "Default calendar to 'Next Working Day'; date chip banner confirmation before submit", "Android / Mobile Team", "0 misdated bookings"),
        ("P0", "GPS / ETA Stalls", "Kalman filter on driver coordinates; Dead reckoning fallback; Driver heartbeat telemetry", "Mobile + Infra Team", "ETA error < 2 mins"),
        ("P1", "0% Reply Rate", "Deploy automated triage bot + Zendesk webhook for 1-2 star reviews; 24h SLA target", "Support / CX Lead", ">80% reply rate in 14d"),
        ("P1", "Android Crashes", "Targeted update for Android 14/15 Foreground Services & WorkManager crash hooks", "Android Eng Team", ">99.5% crash-free rate")
    ]
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            if j == 0:
                p.font.bold = True
                p.font.color.rgb = RED if "P0" in val else PRIMARY
            elif j == 4:
                p.font.bold = True
                p.font.color.rgb = GREEN
            else:
                p.font.color.rgb = TEXT_MAIN

    # -------------------------------------------------------------
    # SLIDE 5: EXECUTION ROADMAP
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Phased Execution Roadmap: Rapid Stabilization", 
               "From fire-fighting P0 fixes to proactive telemetry and review inversion")

    phases = [
        ("Week 1 - 2", "P0 Quick Wins & Stabilization", RED, [
            "Hotfix booking calendar date picker logic",
            "Introduce Driver Geofence check for No-Show button",
            "Set up Zendesk integration for Play Store review replies",
            "Deploy 'playstore_pulse.py' for daily sentiment capture"
        ]),
        ("Week 3 - 4", "Telemetry & Dispute Safety Net", PRIMARY, [
            "Ship 24-hr in-app payroll penalty dispute button",
            "GPS Kalman smoothing + heartbeat reconnect on driver app",
            "Targeted fix for Android 14/15 background service crashes",
            "Reach 80%+ response rate on incoming negative reviews"
        ]),
        ("Month 2", "Experience Polish & Positive Prompts", ACCENT_GOLD, [
            "Redesign seatbelt / OTP confirmation flow",
            "Implement in-app rating prompt triggered only after 3 consecutive 5-star rides",
            "Driver incentive score tied to on-time geofence compliance",
            "Bi-weekly executive review with Enterprise Account Managers"
        ]),
        ("Month 3+", "Sustained Excellence", GREEN, [
            "Automated weekly 'playstore_pulse.py' Slack / Email alert",
            "Maintain 99.5%+ crash-free user rate across all OEM devices",
            "Public Play Store 30-day moving average locked at 4.3+ stars",
            "Zero false payroll penalty complaints escalated to client HR"
        ])
    ]

    pw = Inches(2.7)
    p_gap = Inches(0.3)
    px = Inches(0.8)
    for i, (time_lbl, title, banner_clr, items) in enumerate(phases):
        x = px + i * (pw + p_gap)
        sc = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), pw, Inches(5.3))
        sc.fill.solid(); sc.fill.fore_color.rgb = CARD_BG; sc.line.color.rgb = CARD_BORDER
        stf = sc.text_frame
        stf.margin_left = Inches(0.2); stf.margin_top = Inches(0.2); stf.margin_right = Inches(0.2)
        
        # Banner pill
        bp = stf.paragraphs[0]
        bp.text = time_lbl
        bp.font.bold = True; bp.font.size = Pt(13); bp.font.color.rgb = banner_clr
        bp.space_after = Pt(4)
        
        tp = stf.add_paragraph()
        tp.text = title
        tp.font.bold = True; tp.font.size = Pt(12); tp.font.color.rgb = NAVY
        tp.space_after = Pt(14)

        for item in items:
            ip = stf.add_paragraph()
            ip.text = "✓ " + item
            ip.font.size = Pt(10); ip.font.color.rgb = TEXT_MAIN
            ip.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 6: AUTOMATED RECURRING MONITORING (playstore_pulse.py)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Proactive Monitoring: playstore_pulse.py", 
               "An automated Python tool designed by the FDE to ensure no silent sentiment drops recur")

    # Left: Code snippet / capabilities
    c_left = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c_left.fill.solid(); c_left.fill.fore_color.rgb = DARK_BLUE; c_left.line.color.rgb = RGBColor(51, 65, 85)
    ctfl = c_left.text_frame
    ctfl.margin_left = Inches(0.25); ctfl.margin_top = Inches(0.25); ctfl.margin_right = Inches(0.25)
    
    p = ctfl.paragraphs[0]
    p.text = "Engine Architecture & Pipeline"
    p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = ACCENT_GOLD; p.space_after = Pt(8)

    pipe_steps = [
        ("1. Google Play Scraper Engine:", " Fetches recent 500+ reviews for `com.moveinsync.ets` directly from the Play Store."),
        ("2. Keyword Theme Classifier:", " Multi-label tagging into 8 key themes (No Show, Booking bug, GPS/ETA, Crashes, UI, Support)."),
        ("3. 6-Line Standard Answer:", " Generates an executive-ready weekly status update instantly readable in 10 seconds."),
        ("4. JSON Snapshot History:", " Persists structured snapshots under `/pulse_snapshots` for week-on-week delta tracking."),
        ("5. Tagged CSV Export:", " Exports detailed raw dataset for engineering sprint triage.")
    ]
    for s_t, s_d in pipe_steps:
        sp = ctfl.add_paragraph()
        sp.space_after = Pt(8)
        r1 = sp.add_run(); r1.text = s_t; r1.font.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = WHITE
        r2 = sp.add_run(); r2.text = s_d; r2.font.size = Pt(11); r2.font.color.rgb = RGBColor(203, 213, 225)

    # Right: Sample 6-Line Output
    c_right = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c_right.fill.solid(); c_right.fill.fore_color.rgb = CARD_BG; c_right.line.color.rgb = CARD_BORDER
    ctfr = c_right.text_frame
    ctfr.margin_left = Inches(0.25); ctfr.margin_top = Inches(0.25); ctfr.margin_right = Inches(0.25)

    p = ctfr.paragraphs[0]
    p.text = "Sample Executive 6-Line Weekly Output"
    p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = NAVY; p.space_after = Pt(10)

    sample_output = [
        "1. Current Lifetime Rating : 4.32 / 5.0 (114,528 total)",
        "2. 30-Day Moving Average  : 3.01 / 5.0 (-0.12 vs last week)",
        "3. 1-Star Share (Recent)  : 41.2% of recent ratings",
        "4. Top Negative Theme     : No Show / penalty (43% of 1-star)",
        "5. Emerging Spike         : Booking date bug (+14% WoW)",
        "6. Recommended P0 Action  : Enforce Driver Geofence check"
    ]
    for line in sample_output:
        lp = ctfr.add_paragraph()
        lp.text = line
        lp.font.size = Pt(11); lp.font.color.rgb = PRIMARY; lp.font.bold = True
        lp.space_after = Pt(6)

    rp_run = ctfr.add_paragraph()
    rp_run.text = "\nRun locally anytime in 1 step:\n$ python playstore_pulse.py"
    rp_run.font.size = Pt(11); rp_run.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 7: PROJECTED IMPACT & BUSINESS VALUE
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Projected Impact: Quantifiable Turnaround Targets", 
               "60-day recovery trajectory across app rating, user trust, and enterprise SLAs")

    impact_cards = [
        ("30-Day Rolling Rating", "~3.0 Stars", "4.3+ Stars", "Achieved by eliminating top 3 penalty & booking bugs causing 70% of 1-star reviews", GREEN),
        ("1-Star Review Share", "12% Lifetime (40% recent)", "< 8%", "Preventing accidental no-show deductions removes the #1 user trigger to leave 1 star", GREEN),
        ("Play Store Developer Reply Rate", "Near 0%", "> 80% in 24h", "Closing the loop turns 1-star reviews into updated 4 or 5-star reviews (industry avg 20-30% flip)", GREEN),
        ("Crash-Free User Sessions", "~97.2%", "> 99.5%", "Resolved via background location foreground service patch on Android 14/15", GREEN)
    ]

    for i, (metric, current_val, target_val, explanation, clr) in enumerate(impact_cards):
        y = Inches(1.5) + i * Inches(1.3)
        c = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.15))
        c.fill.solid(); c.fill.fore_color.rgb = CARD_BG; c.line.color.rgb = CARD_BORDER
        ctf = c.text_frame
        ctf.margin_left = Inches(0.25); ctf.margin_top = Inches(0.12); ctf.margin_right = Inches(0.25)
        
        p = ctf.paragraphs[0]
        r1 = p.add_run(); r1.text = metric; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = f"   Current: {current_val}   ->   Target: {target_val}"; r2.font.bold = True; r2.font.size = Pt(12); r2.font.color.rgb = clr
        
        p2 = ctf.add_paragraph()
        p2.text = explanation
        p2.font.size = Pt(10.5); p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 8: SUMMARY & FDE PERSPECTIVE
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Conclusion: The Forward Deployed Engineer Mindset", 
               "Bridging customer frustration, software engineering, and corporate operations")

    sc_left = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    sc_left.fill.solid(); sc_left.fill.fore_color.rgb = CARD_BG; sc_left.line.color.rgb = CARD_BORDER
    stf = sc_left.text_frame
    stf.margin_left = Inches(0.3); stf.margin_top = Inches(0.3); stf.margin_right = Inches(0.3)
    
    p = stf.paragraphs[0]
    p.text = "Why an FDE Solves This Differently"
    p.font.bold = True; p.font.size = Pt(17); p.font.color.rgb = NAVY; p.space_after = Pt(10)

    fde_points = [
        ("Listens at the Ground Level:", " Reads Play Store complaints not as noise, but as high-fidelity operational signal."),
        ("Fixes the Incentive Misalignment:", " Drivers marked No-Show to hit trip quotas; introducing geofence bounds realigns field behavior."),
        ("Builds Tooling, Not Just Spreadsheets:", " Delivered `playstore_pulse.py` so product and engineering have continuous visibility."),
        ("Protects Enterprise Contracts:", " Happy employees mean satisfied corporate HR clients and protected renewal revenue.")
    ]
    for pt, pdesc in fde_points:
        pp = stf.add_paragraph()
        pp.space_after = Pt(10)
        r = pp.add_run(); r.text = "• " + pt; r.font.bold = True; r.font.size = Pt(12); r.font.color.rgb = PRIMARY
        r2 = pp.add_run(); r2.text = pdesc; r2.font.size = Pt(11); r2.font.color.rgb = TEXT_MAIN

    sc_right = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    sc_right.fill.solid(); sc_right.fill.fore_color.rgb = NAVY; sc_right.line.color.rgb = RGBColor(30, 41, 59)
    stfr = sc_right.text_frame
    stfr.margin_left = Inches(0.3); stfr.margin_top = Inches(0.3); stfr.margin_right = Inches(0.3)

    p = stfr.paragraphs[0]
    p.text = "Complete Submission Deliverables"
    p.font.bold = True; p.font.size = Pt(17); p.font.color.rgb = ACCENT_GOLD; p.space_after = Pt(12)

    delivs = [
        ("📄 Comprehensive PDF Report:", " MoveInSync_FDE_Submission_Improved.pdf (8 pages, charts, tables)"),
        ("📊 Executive Presentation Deck:", " MoveInSync_FDE_Presentation_Deck.pptx (8 widescreen slides)"),
        ("⚡ Python Monitoring Script:", " playstore_pulse.py (automated scrapers, NLP categorization, snapshots)"),
        ("🌐 Interactive Web Dashboard:", " Live review triage simulator, sentiment analytics & recovery model"),
        ("🔗 GitHub Repository:", " https://github.com/Rudra152005/MoveInCaseStudy")
    ]
    for d_t, d_d in delivs:
        dp = stfr.add_paragraph()
        dp.space_after = Pt(8)
        r = dp.add_run(); r.text = d_t; r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = WHITE
        r2 = dp.add_run(); r2.text = d_d; r2.font.size = Pt(10.5); r2.font.color.rgb = RGBColor(203, 213, 225)

    out_file = "MoveInSync_FDE_Presentation_Deck.pptx"
    prs.save(out_file)
    print(f"Successfully generated {out_file} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    create_deck()
