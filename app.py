import os
import re
import requests
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = Flask(__name__)

# ==========================================
# 🛠️ HARDCORE CONFIGURATIONS (INTEGRATION MATRIX)
# ==========================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "YOUR_API_HERE")

# Flask-Mail / SMTP Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''       # <-- Sender/System Email
app.config['MAIL_PASSWORD'] = ''           # <-- Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = ''

mail = Mail(app)

ADMIN_EMAIL = ""           # <-- Admin Ki Email Target Id

# ==========================================
# 📄 AUTOMATED PDF GENERATOR FUNCTION
# ==========================================
def generate_incident_pdf(filename, job_name, build_number, error_code, ai_text):
    """
    SRE Core Analytics text data ko standard responsive corporate layout PDF me compile karta hai.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'PDFTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#0f172a"), spaceAfter=15
    )
    section_style = ParagraphStyle(
        'PDFSection', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor("#1e3a8a"), spaceBefore=15, spaceAfter=5
    )
    body_style = ParagraphStyle(
        'PDFBody', parent=styles['BodyText'], fontSize=10, textColor=colors.HexColor("#334155"), leading=14
    )

    # Document Header Title
    story.append(Paragraph("🛡️ JURIXAI X SYNTAX SQUAD — OFFICIAL SRE INCIDENT REPORT", title_style))
    story.append(Spacer(1, 10))

    # System Meta Framework Table
    table_data = [
        [Paragraph("<b>PROJECT PLATFORM:</b>", body_style), Paragraph("JurixAI Core System Suite", body_style)],
        [Paragraph("<b>FAILING PIPELINE:</b>", body_style), Paragraph(f"{job_name} (Build #{build_number})", body_style)],
        [Paragraph("<b>ERROR CATEGORY:</b>", body_style), Paragraph(error_code, body_style)],
        [Paragraph("<b>TRIAGE OWNER:</b>", body_style), Paragraph("Syntax Squad 🛡️", body_style)],
        [Paragraph("<b>DIAGNOSTIC ENGINE:</b>", body_style), Paragraph("Jurix SRE Kernel v2.0", body_style)]
    ]

    meta_table = Table(table_data, colWidths=[140, 360])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Clean text payload indicators for PDF printing
    story.append(Paragraph("ROOT CAUSE ANALYSIS & ACTIONS RESOLUTION SUMMARY:", section_style))
    story.append(Spacer(1, 5))

    # 🔥 🛠️ BULLETPROOF REPORTLAB PDF PARSER SANITIZATION LAYER 🔥
    # Saare classes, divs, spans aur invalid attributes ko completely clean/convert karega taaki ReportLab crash na ho
    clean_text = ai_text
    clean_text = re.sub(r'<div[^>]*>', '', clean_text)
    clean_text = re.sub(r'</div>', '\n', clean_text)
    clean_text = re.sub(r'<span[^>]*>', '<b>', clean_text)
    clean_text = re.sub(r'</span>', '</b> ', clean_text)
    clean_text = re.sub(r'<h3[^>]*>', '\n<b><font size="12">', clean_text)
    clean_text = re.sub(r'</h3>', '</font></b>\n', clean_text)
    clean_text = re.sub(r'<h4[^>]*>', '\n<b>', clean_text)
    clean_text = re.sub(r'</h4>', '</b>\n', clean_text)
    clean_text = re.sub(r'<ul>', '', clean_text)
    clean_text = re.sub(r'</ul>', '', clean_text)
    clean_text = re.sub(r'<li>', '• ', clean_text)
    clean_text = re.sub(r'</li>', '\n', clean_text)
    clean_text = re.sub(r'<code>', ' [ ', clean_text)
    clean_text = re.sub(r'</code>', ' ] ', clean_text)

    for block in clean_text.split('\n'):
        if block.strip():
            story.append(Paragraph(block.strip(), body_style))
            story.append(Spacer(1, 4))

    doc.build(story)

# ==========================================
# 🧠 CORE ENGINE UTILITY (GROQ RUNTIME LOOP)
# ==========================================
def run_sre_ai_engine(job_name, build_number, cleaned_logs):
    """
    Logs metadata ko Llama-3.3 Core model ke sath dynamic query hit process karta hai.
    """
    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    ai_prompt = f"""
    You are an elite DevOps SRE Expert. Analyze this Jenkins failure and generate a high-fidelity summary report.
    Write completely in Hinglish with premium tech emojis. Format strictly using structural clean HTML tags.

    STRUCTURE YOUR RESPONSE EXACTLY LIKE THIS:
    - <h3>📋 [1] JURIXAI X SYNTAX SQUAD SUMMARY REPORT</h3>
      <div class="summary-card">
          <div class="summary-header"><h4>📊 LIVE PIPELINE FAULT SNAPSHOT</h4><span class="badge badge-danger">CRITICAL ERROR</span></div>
          <div class="summary-grid">
              <div class="summary-item"><span class="s-label">FAILING NODE:</span><span class="s-value text-cyan">{job_name}</span></div>
              <div class="summary-item"><span class="s-label">BUILD ID:</span><span class="s-value text-pink">Build #{build_number}</span></div>
              <div class="summary-item"><span class="s-label">DIAGNOSTIC ENGINE:</span><span class="s-value" style="color: var(--accent-purple);">JurixAI SRE Engine v2.0</span></div>
              <div class="summary-item"><span class="s-label">TRIAGE OWNER:</span><span class="s-value">Syntax Squad 🛡️</span></div>
           Welch parameters or style details
          </div>
      </div>
    - <h3>🔍 [2] REASON KYA THA? (ROOT CAUSE ANALYSIS)</h3>
      Give precise bullet points in Hinglish explaining *why* it failed. Use premium tech emojis.
    - <h3>🛠️ [3] EXACT 3-STEP FIX (REMEDIATION PLAYBOOK)</h3>
      Provide exactly 3 copy-pasteable resolution steps. Short description in Hinglish followed by direct command wrapped inside <code> tags.

    RAW CRASH ENVIRONMENT TRACE LOGS:
    {cleaned_logs}
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a precise automated SRE diagnostic backend node. You output structural alerts context in Hinglish with raw HTML elements."},
            {"role": "user", "content": ai_prompt}
        ],
        "temperature": 0.15,
        "max_tokens": 900
    }

    response = requests.post(groq_url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# ==========================================
# 🚀 CORE WEB ROUTES & WEBHOOK PORTAL
# ==========================================

@app.route('/')
def home():
    """
    Landing Route — Direct templates folder se dashboard layout index.html parse karega.
    """
    return render_template('index.html')

@app.route('/webhook/jenkins-failure', methods=['POST'])
def jenkins_failure_webhook():
    """
    Jenkins post-action runtime automation failure endpoint trigger layer.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No payload bundle received"}), 400

        job_name = data.get('job_name', 'Remote Jenkins Project')
        build_number = data.get('build_number', '0')
        raw_logs = data.get('logs', 'Empty log stream parameter.')

        print(f"🚨 WEBHOOK ACTIVE: Live failure catch in {job_name} | Build #{build_number}")

        # 💾 📁 AUTOMATIC LOCAL FILE SYNC LAYER (For Dashboard Automations)
        if not os.path.exists('logs'):
            os.makedirs('logs')
        with open('logs/jenkins_output.log', 'w', encoding='utf-8') as log_file:
            log_file.write(raw_logs)
        print("💾 [AUTOMATIC] Live Jenkins logs written to logs/jenkins_output.log successfully.")

        # Optimize boundary parameters (Slicing last 120 lines logs)
        log_lines = raw_logs.split('\n')[-120:]
        cleaned_logs = "\n".join(log_lines)

        # Invoke AI Execution
        ai_solution = run_sre_ai_engine(job_name, build_number, cleaned_logs)

        # Compile PDF Attachment (Iske andar automatic filter sanitize karega ab!)
        pdf_filename = f"Incident_Report_Build_{build_number}.pdf"
        generate_incident_pdf(pdf_filename, job_name, build_number, "Jenkins Pipeline Automation Crash", ai_solution)

        # Email Dispatch System HTML Mail Frame
        email_html = f"""
        <div style="background-color: #0b0f19; color: #e2e8f0; padding: 25px; font-family: sans-serif; border-radius: 12px; max-width: 600px; margin: auto; border: 1px solid #1e293b;">
            <h2 style="color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 8px; margin-bottom: 15px;">🚨 PIPELINE CRITICAL RUNTIME ERROR REPORT</h2>
            <p style="font-size: 14px; color: #94a3b8;">
                Bhai, live execution node par pipeline <b>{job_name} (Build #{build_number})</b> crash ho gayi hai.
                Jurix SRE AI ne immediate diagnostic analysis execute karke summary template generate kar diya hai:
            </p>
            <div style="background-color: #111827; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #ef4444; color: #f1f5f9;">
                {ai_solution}
            </div>
            <p style="font-size: 11px; color: #64748b; margin-top: 20px; text-align: center; border-top: 1px solid #1e293b; padding-top: 10px;">
                Official incident evaluation report PDF document format me attached hai.<br>
                Generated by <b>Syntax Squad 🛡️</b> via JurixAI System Core.
            </p>
        </div>
        """

        msg = Message(
            subject=f"🚨 LIVE CRITICAL FAILURE: Jenkins Alert in {job_name} (Build #{build_number})",
            recipients=[ADMIN_EMAIL],
            html=email_html
        )

        # Read and attach compiled PDF file stream
        with open(pdf_filename, "rb") as pdf_file:
            msg.attach(filename=pdf_filename, content_type="application/pdf", data=pdf_file.read())

        mail.send(msg)
        print("📧 [SUCCESS] SRE Evaluation PDF dispatched securely to Admin inbox!")

        # Server memory cleanup step
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)

        return jsonify({"status": "success", "message": "Webhook processed, PDF attached and email sent safely!"}), 200

    except Exception as err:
        print(f"🚨 WEBHOOK LAYER FAILURE EXCEPTION: {str(err)}")
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route('/analyze-file', methods=['POST'])
def analyze_local_file():
    """
    Dashboard button trigger fallback route logic (reads local logs directory file).
    """
    try:
        log_path = "logs/jenkins_output.log"
        if not os.path.exists(log_path):
            return jsonify({"status": "error", "message": f"Target file '{log_path}' missing in filesystem bounds"}), 404

        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-120:]
        cleaned_logs = "".join(lines)

        ai_solution = run_sre_ai_engine("Local Static Dashboard Scan", "N/A", cleaned_logs)
        return jsonify({"status": "success", "analysis": ai_solution}), 200

    except Exception as file_err:
        return jsonify({"status": "error", "message": str(file_err)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
