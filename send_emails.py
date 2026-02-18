import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd
import os
import time
from datetime import datetime

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "blockchainclub@vitbhopal.ac.in"
EMAIL_PASSWORD = "dgul wazj evka null"  # App password
BCC_EMAIL = "blockchainclub@vitbhopal.ac.in"

def send_email(recipient_email, registration_number, name, ticket_path):
    """Send email with ticket attachment to a recipient"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Bcc'] = BCC_EMAIL
        msg['Subject'] = "Your Ticket for the Blockchain Club Event - Decrypt2Win"
        
        # Email content in HTML format
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
        }}
        .event-details {{
            background: white;
            padding: 20px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .event-details h3 {{
            color: #667eea;
            margin-top: 0;
        }}
        .highlight {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            text-align: center;
        }}
        .social-links {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            text-align: center;
        }}
        .social-links h4 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        .social-links a {{
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
            margin: 0 10px;
            display: inline-block;
            padding: 5px 10px;
            border: 1px solid #667eea;
            border-radius: 5px;
            margin-bottom: 10px;
        }}
        .social-links a:hover {{
            background: #667eea;
            color: white;
        }}
        .footer {{
            background: #667eea;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 0 0 10px 10px;
        }}
        .registration {{
            font-family: monospace;
            font-size: 14px;
            color: #666;
            text-align: center;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🎯 Decrypt2Win - Your Official Ticket</h2>
        <p>Blockchain Club VIT Bhopal</p>
    </div>
    
    <div class="content">
        <p><strong>Dear {name},</strong></p>
        
        <p>The time has come! We are excited to welcome you to the <strong>Blockchain Club's</strong> highly anticipated event.</p>
        
        <p>This is your <strong>official ticket</strong> to an engaging session featuring our unique <strong>Blockchain Tambola game</strong>, and a valuable <strong>AMA (Ask Me Anything)</strong> session with a successful alumnus who achieved a remarkable <strong>56 LPA package</strong>.</p>
        
        <div class="event-details">
            <h3>📅 Event Details</h3>
            <p><strong>📆 Date & Time:</strong> September 20th, 10:30 AM</p>
            <p><strong>📍 Venue:</strong> AB02 Auditorium-2 (First floor)</p>
            <p><strong>🎫 Ticket:</strong> This email serves as your ticket for entry</p>
        </div>
        
        <div class="highlight">
            <p><strong>⚠️ Important:</strong> Please bring your laptop for the event.</p>
        </div>
        
        <p>We can't wait to see you there for a day of learning, interaction, and inspiration.</p>
        
        <div class="social-links">
            <h4>🌐 Let's Stay Connected</h4>
            <p>Follow us for updates and future events:</p>
            <div>
                <a href="https://linkedin.com/company/blockchain-club-vitb/">LinkedIn</a>
                <a href="https://instagram.com/blockchain.vitb/">Instagram</a>
                <a href="https://x.com/blockchainvitb">X (Twitter)</a>
                <a href="https://youtube.com/@blockchainclubvitb">YouTube</a>
            </div>
            <div style="margin-top: 10px;">
                <a href="https://chat.whatsapp.com/KI3mnptIqiR6gTgv0grRJG">WhatsApp Community</a>
            </div>
            <p style="margin-top: 15px; font-size: 12px; color: #666;">
                Share your experience with: <strong>#BlockchainClubVITB #Decrypt2Win #VITBhopal</strong>
            </p>
        </div>
    </div>
    
    <div class="footer">
        <p><strong>Best Regards,</strong><br>
        Blockchain Club<br>
        VIT Bhopal University</p>
        
        <div class="registration">
            Registration Number: {registration_number}
        </div>
    </div>
</body>
</html>
"""
        
        # Create plain text version for email clients that don't support HTML
        text_body = f"""Dear {name},

The time has come! We are excited to welcome you to the Blockchain Club's highly anticipated event.

This is your official ticket to an engaging session featuring our unique Blockchain Tambola game, and a valuable AMA (Ask Me Anything) session with a successful alumnus who achieved a remarkable 56 LPA package.

EVENT DETAILS:
📅 Date & Time: September 20th, 10:30 AM
📍 Venue: AB02 Auditorium-2 (First floor)
🎫 Ticket: This email serves as your ticket for entry

⚠️ IMPORTANT: Please bring your laptop for the event.

We can't wait to see you there for a day of learning, interaction, and inspiration.

STAY CONNECTED:
LinkedIn: https://linkedin.com/company/blockchain-club-vitb/
Instagram: https://instagram.com/blockchain.vitb/
X (Twitter): https://x.com/blockchainvitb
YouTube: https://youtube.com/@blockchainclubvitb
WhatsApp Community: https://chat.whatsapp.com/KI3mnptIqiR6gTgv0grRJG

Share your experience with: #BlockchainClubVITB #Decrypt2Win #VITBhopal

Best Regards,
Blockchain Club
VIT Bhopal University

Registration Number: {registration_number}
"""
        
        # Attach both HTML and plain text versions
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Attach ticket image if it exists
        if os.path.exists(ticket_path):
            with open(ticket_path, 'rb') as f:
                img_data = f.read()
                image = MIMEImage(img_data)
                image.add_header('Content-Disposition', 
                               f'attachment; filename="{registration_number}_ticket.png"')
                msg.attach(image)
        else:
            print(f"Warning: Ticket file not found for {registration_number}: {ticket_path}")
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable security
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, [recipient_email, BCC_EMAIL], text)
        server.quit()
        
        # Log success
        log_message = f"[{datetime.now()}] SUCCESS: Email sent to {recipient_email} ({name}) - Registration: {registration_number}"
        print(log_message)
        
        with open('email_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_message + "\n")
            
        return True
        
    except Exception as e:
        # Log error
        error_message = f"[{datetime.now()}] ERROR: Failed to send email to {recipient_email} ({name}) - {str(e)}"
        print(error_message)
        
        with open('email_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(error_message + "\n")
            
        return False

def process_csv_and_send_emails(csv_file='assets/data.csv', ticket_folder='output/tickets', delay_seconds=5):
    """Read CSV file and send emails to all participants"""
    
    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        return
    
    # Check if ticket folder exists
    if not os.path.exists(ticket_folder):
        print(f"Error: Ticket folder not found: {ticket_folder}")
        return
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        print(f"Found {len(df)} participants in the CSV file")
        print(f"Starting email sending process...")
        print(f"Delay between emails: {delay_seconds} seconds")
        print("-" * 50)
        
        # Initialize counters
        success_count = 0
        error_count = 0
        
        # Process each row
        for index, row in df.iterrows():
            try:
                # Extract data from CSV
                email = row['Email'].strip()
                registration_number = row['Registration'].replace(" ", "").upper()
                name = row['Name'].strip()
                
                # Construct ticket file path
                ticket_path = os.path.join(ticket_folder, f"{registration_number}.png")
                
                print(f"Processing {index + 1}/{len(df)}: {name} ({registration_number})")
                
                # Send email
                if send_email(email, registration_number, name, ticket_path):
                    success_count += 1
                else:
                    error_count += 1
                
                # Add delay between emails to avoid rate limiting
                if index < len(df) - 1:  # Don't delay after the last email
                    print(f"Waiting {delay_seconds} seconds before next email...")
                    time.sleep(delay_seconds)
                    
            except Exception as e:
                error_message = f"Error processing row {index + 1}: {str(e)}"
                print(error_message)
                
                with open('email_log.txt', 'a', encoding='utf-8') as log_file:
                    log_file.write(f"[{datetime.now()}] {error_message}\n")
                
                error_count += 1
        
        # Final summary
        print("-" * 50)
        print(f"Email sending completed!")
        print(f"Total participants: {len(df)}")
        print(f"Successful emails: {success_count}")
        print(f"Failed emails: {error_count}")
        print(f"Check 'email_log.txt' for detailed logs")
        
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")

if __name__ == "__main__":
    print("Blockchain Club Event - Email Sender")
    print("=" * 40)
    
    # Configuration
    csv_file = 'assets/data.csv'
    ticket_folder = 'output/tickets'
    delay_seconds = 5  # Adjust delay as needed (5 seconds recommended)
    
    # Confirm before sending
    print(f"CSV File: {csv_file}")
    print(f"Ticket Folder: {ticket_folder}")
    print(f"Delay between emails: {delay_seconds} seconds")
    print(f"BCC Email: {BCC_EMAIL}")
    print()
    
    response = input("Do you want to proceed with sending emails? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        process_csv_and_send_emails(csv_file, ticket_folder, delay_seconds)
    else:
        print("Email sending cancelled.")