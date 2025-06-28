# Cold Email Sender

A Flask web application for sending personalized cold emails to recruiters and HR professionals with resume attachments.

## Features

- **Personalized Emails**: Auto-personalizes emails using recipient's first name and company
- **Resume Attachment**: Automatically attaches your resume to each email
- **CSV Import**: Upload contact lists in CSV format (Name, Company, Email)
- **Custom Templates**: Editable email templates with placeholder support
- **Spam Prevention**: Built-in delays and retry logic for better deliverability
- **Modern UI**: Clean, responsive interface built with Bootstrap

## Quick Start

### Prerequisites
- Python 3.7+
- Gmail account with App Password (or other SMTP provider)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd cold-mailer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure email settings**
   Edit `config.py` with your email credentials:
   ```python
   EMAIL_CONFIG = {
       'smtp_server': 'smtp.gmail.com',
       'smtp_port': 587,
       'sender_email': 'your-email@gmail.com',
       'sender_password': 'your-app-password'
   }
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   Open http://127.0.0.1:5001 in your browser

## Usage

### 1. Prepare Your Data
- Create a CSV file with columns: `Name`, `Company`, `Email`
- Example:
  ```
  Name,Company,Email
  John Smith,Google,john.smith@google.com
  Sarah Johnson,Microsoft,sarah.j@microsoft.com
  ```

### 2. Upload Files
- Upload your contacts CSV file
- Upload your resume (PDF format)

### 3. Customize Email
- Edit your personal information (name, phone, email)
- Customize the email template if needed
- Preview how emails will look

### 4. Send Emails
- Review the preview of your first 10 contacts
- Click "Send Emails" to start the campaign
- Monitor progress in the console

## Email Template

The default template includes:
- Personalized greeting with first name
- Professional introduction
- Mention of your background (Cisco Meraki internship)
- Call to action
- Contact information

**Available placeholders:**
- `{recipient_name}` - Recipient's first name
- `{company_name}` - Company name
- `{your_name}` - Your name
- `{your_phone}` - Your phone number
- `{your_email}` - Your email address

## Configuration

### Email Settings (`config.py`)
- SMTP server configuration
- Email template customization
- Sending limits and delays

### Sending Limits
- **Per session**: 25 emails (configurable)
- **Delay between emails**: 5 seconds
- **Daily limit**: 100 emails
- **Retry attempts**: 3 per email

## Security Notes

- Use App Passwords for Gmail (not your regular password)
- Enable 2-Factor Authentication on your email account
- Never commit email credentials to version control
- Consider using environment variables for sensitive data

## File Structure

```
cold-mailer/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── index.html     # Main interface
│   └── preview.html   # Email preview and sending
├── uploads/           # Temporary file storage
└── README.md         # This file
```

## Troubleshooting

### Common Issues

1. **"Address already in use"**
   - The app runs on port 5001 to avoid macOS AirPlay conflicts
   - If port 5001 is busy, change the port in `app.py`

2. **Email sending fails**
   - Verify your SMTP settings in `config.py`
   - Check that you're using an App Password for Gmail
   - Ensure 2-Factor Authentication is enabled

3. **CSV upload errors**
   - Ensure your CSV has the correct column headers: `Name`, `Company`, `Email`
   - Check that email addresses are valid

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This tool is designed for legitimate job applications. Please use responsibly and in compliance with email marketing laws and best practices. 