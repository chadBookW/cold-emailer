# Cold Email Sender

A modern Flask web application for sending personalized cold emails to HR professionals and recruiters with automatic resume attachments.

## ✨ Features

- 📧 **Personalized Emails**: Automatically personalize emails with recipient name and company
- 📎 **Resume Upload**: Upload your resume directly in the app
- 📊 **CSV Upload**: Upload your contact list in CSV format
- ✏️ **Editable Template**: Customize your email template in real-time
- 👀 **Live Preview**: See how your emails will look before sending
- 🚫 **Duplicate Prevention**: Automatically removes duplicate contacts
- ⏱️ **Spam Prevention**: Built-in delays and limits to avoid spam detection
- 🎨 **Modern UI**: Beautiful, responsive web interface

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Configure Email Settings
Edit `config.py` and update:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password'
}
```

### 3. Start the Application
```bash
python3 app.py
```

### 4. Open Your Browser
Navigate to: http://localhost:5001

## 📧 Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
3. **Use the App Password** in config.py (not your regular password)

## 📁 CSV Format

Your CSV should have these columns:
```csv
Name,Company,Email
John Smith,Google,hr@google.com
Jane Doe,Microsoft,recruiter@microsoft.com
```

## 🎯 How to Use

1. **Upload Files**: Upload your CSV contacts and resume PDF
2. **Customize Template**: Edit your email template with placeholders
3. **Preview Data**: Review your contacts and email preview
4. **Configure Info**: Fill in your personal information
5. **Send Emails**: Send personalized emails with resume attached

## 🔧 Email Template Placeholders

Use these placeholders in your email template:
- `{recipient_name}` - Recipient's name
- `{company_name}` - Company name
- `{your_name}` - Your name
- `{your_title}` - Your job title
- `{your_skills}` - Your skills
- `{your_phone}` - Your phone number
- `{your_email}` - Your email address

## ⚙️ Configuration

### Email Settings
- **SMTP Server**: Your email provider's SMTP server
- **Port**: Usually 587 for TLS
- **App Password**: Use app password, not regular password

### Spam Prevention
- **Delay**: 5 seconds between emails
- **Session Limit**: 25 emails per session
- **Daily Limit**: 100 emails per day
- **Retry Attempts**: 3 attempts for failed emails

## 📊 Supported Email Providers

- **Gmail**: `smtp.gmail.com:587`
- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`

## 🛡️ Security & Best Practices

- ✅ Use App Passwords for Gmail
- ✅ Enable 2-Factor Authentication
- ✅ Start with small batches
- ✅ Monitor delivery rates
- ✅ Follow email marketing laws
- ❌ Don't exceed daily limits
- ❌ Avoid spam trigger words

## 📝 File Structure

```
cold-mailer/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── index.html     # Main upload page
│   └── preview.html   # Preview and send page
├── uploads/           # Uploaded files (auto-created)
└── README.md          # This file
```

## 🆘 Troubleshooting

### Common Issues
1. **Port 5000 in use**: App runs on port 5001 to avoid AirPlay conflict
2. **Gmail authentication**: Use App Password, not regular password
3. **CSV format**: Ensure columns are Name, Company, Email
4. **Resume upload**: Must be PDF format

### Error Messages
- **"Username and Password not accepted"**: Use App Password
- **"Missing required columns"**: Check CSV format
- **"Resume must be a PDF"**: Convert resume to PDF

## 📄 License

This project is for educational purposes. Use responsibly and in compliance with applicable laws and email service provider terms of service.

---

**Ready to send personalized cold emails?** 🚀

Start the app and upload your contacts! 