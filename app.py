from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import csv
from datetime import datetime
import logging
import time
from config import EMAIL_CONFIG, EMAIL_TEMPLATE, APP_CONFIG, SENDING_CONFIG
import shutil

app = Flask(__name__)
app.secret_key = APP_CONFIG['secret_key']

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store uploaded files
uploaded_resume = None
uploaded_csv_data = None

@app.route('/')
def index():
    from config import EMAIL_TEMPLATE
    return render_template('index.html', config={'EMAIL_TEMPLATE': EMAIL_TEMPLATE})

@app.route('/upload_files', methods=['POST'])
def upload_files():
    global uploaded_resume, uploaded_csv_data
    
    # Handle CSV upload
    if 'csv_file' not in request.files:
        flash('No CSV file selected', 'error')
        return redirect(url_for('index'))
    
    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        flash('No CSV file selected', 'error')
        return redirect(url_for('index'))
    
    if not csv_file.filename.endswith('.csv'):
        flash('Please upload a CSV file', 'error')
        return redirect(url_for('index'))
    
    # Handle resume upload
    resume_file = request.files.get('resume_file')
    if resume_file and resume_file.filename != '':
        if not resume_file.filename.lower().endswith('.pdf'):
            flash('Resume must be a PDF file', 'error')
            return redirect(url_for('index'))
        
        # Save resume
        resume_filename = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        resume_path = os.path.join('uploads', resume_filename)
        os.makedirs('uploads', exist_ok=True)
        resume_file.save(resume_path)
        uploaded_resume = resume_path
        flash(f'Resume uploaded: {resume_file.filename}', 'success')
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Handle different CSV formats
        if len(df.columns) >= 3:
            # Check if it's the user's format: Name,Company,Email
            if 'Name' in df.columns and 'Company' in df.columns and 'Email' in df.columns:
                # Rename columns to match our expected format
                df = df.rename(columns={
                    'Name': 'name',
                    'Company': 'company', 
                    'Email': 'email'
                })
            elif 'name' in df.columns and 'company' in df.columns and 'email' in df.columns:
                # Already in correct format
                pass
            else:
                # Try to map first 3 columns to name, company, email
                df.columns = ['name', 'company', 'email'] + list(df.columns[3:])
        else:
            flash('CSV must have at least 3 columns (name, company, email)', 'error')
            return redirect(url_for('index'))
        
        # Clean the data
        df = df.dropna(subset=['email'])  # Remove rows with no email
        df = df[df['email'].str.contains('@', na=False)]  # Keep only valid emails
        
        # Remove duplicates based on email
        df = df.drop_duplicates(subset=['email'])
        
        # Store the data
        uploaded_csv_data = df.to_dict('records')
        
        flash(f'Successfully uploaded {len(uploaded_csv_data)} unique email addresses', 'success')
        from config import EMAIL_TEMPLATE
        return render_template('preview.html', 
                             emails=uploaded_csv_data[:10], 
                             total_count=len(uploaded_csv_data),
                             has_resume=uploaded_resume is not None,
                             config={'EMAIL_TEMPLATE': EMAIL_TEMPLATE})
        
    except Exception as e:
        flash(f'Error reading CSV file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/send_emails', methods=['POST'])
def send_emails():
    global uploaded_resume, uploaded_csv_data
    
    if not uploaded_csv_data:
        flash('No CSV data found. Please upload your contacts first.', 'error')
        return redirect(url_for('index'))
    
    # Get form data
    your_name = request.form.get('your_name', 'Your Name')
    your_phone = request.form.get('your_phone', 'Your Phone')
    your_email = request.form.get('your_email', 'your-email@example.com')
    
    # Get custom email template
    custom_template = request.form.get('email_template', EMAIL_TEMPLATE)
    
    try:
        emails_sent = 0
        failed_emails = []
        
        # Limit emails per session
        max_emails = min(len(uploaded_csv_data), SENDING_CONFIG['max_emails_per_session'])
        df_data = uploaded_csv_data[:max_emails]
        
        for index, row in enumerate(df_data):
            try:
                # Personalize the email
                # Extract first name from full name
                first_name = row['name'].split()[0] if row['name'] else row['name']
                
                personalized_message = custom_template.format(
                    recipient_name=first_name,
                    company_name=row['company'],
                    your_name=your_name,
                    your_phone=your_phone,
                    your_email=your_email
                )
                
                # Send email with retry logic
                success = False
                for attempt in range(SENDING_CONFIG['retry_attempts']):
                    success = send_email(
                        to_email=row['email'],
                        subject=f"Interest in Opportunities at {row['company']}",
                        message=personalized_message,
                        recipient_name=row['name'],
                        resume_path=uploaded_resume
                    )
                    if success:
                        break
                    time.sleep(1)  # Wait before retry
                
                if success:
                    emails_sent += 1
                    logger.info(f"Email {emails_sent}/{max_emails} sent successfully to {row['email']}")
                else:
                    failed_emails.append(row['email'])
                    logger.error(f"Failed to send email to {row['email']} after {SENDING_CONFIG['retry_attempts']} attempts")
                
                # Add delay between emails to avoid spam
                if index < len(df_data) - 1:  # Don't delay after the last email
                    time.sleep(SENDING_CONFIG['delay_between_emails'])
                    
            except Exception as e:
                logger.error(f"Error sending email to {row['email']}: {str(e)}")
                failed_emails.append(row['email'])
        
        flash(f'Successfully sent {emails_sent} emails. Failed: {len(failed_emails)}', 'success')
        if failed_emails:
            flash(f'Failed emails: {", ".join(failed_emails[:5])}', 'warning')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error processing emails: {str(e)}', 'error')
        return redirect(url_for('index'))

def send_email(to_email, subject, message, recipient_name, resume_path=None):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(message, 'plain'))
        
        # Attach resume if provided
        if resume_path and os.path.exists(resume_path):
            with open(resume_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(resume_path)}'
            )
            msg.attach(part)
            logger.info(f"Resume attached: {os.path.basename(resume_path)}")
        else:
            logger.warning("No resume file to attach")
        
        # Create SMTP session
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], to_email, text)
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

@app.route('/download_template')
def download_template():
    """Download CSV template"""
    template_data = [
        {'name': 'John Smith', 'company': 'Company 1', 'email': 'hr@company1.com'},
        {'name': 'Jane Doe', 'company': 'Company 2', 'email': 'recruiter@company2.com'},
        {'name': 'Mike Johnson', 'company': 'Company 3', 'email': 'hiring@company3.com'}
    ]
    
    response = app.response_class(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=email_template.csv'}
    )
    
    writer = csv.DictWriter(response.stream, fieldnames=['name', 'company', 'email'])
    writer.writeheader()
    writer.writerows(template_data)
    
    return response

@app.route('/clear_data', methods=['POST'])
def clear_data():
    """Clear uploaded data"""
    global uploaded_resume, uploaded_csv_data
    
    # Remove uploaded resume
    if uploaded_resume and os.path.exists(uploaded_resume):
        try:
            os.remove(uploaded_resume)
        except:
            pass
    
    uploaded_resume = None
    uploaded_csv_data = None
    
    flash('Uploaded data cleared successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(
        debug=APP_CONFIG['debug'],
        host=APP_CONFIG['host'],
        port=5001  # Changed to avoid AirPlay conflict
    ) 