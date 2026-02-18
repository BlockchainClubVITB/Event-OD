import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
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

# File paths (UNCHANGED)
INPUT_CSV_FILE = r'C:\personal dg\github_repo\Event-OD\Letters-dataset\new-members\new.csv'
PDF_FOLDER = r'C:\personal dg\github_repo\Event-OD\Appointment-letters\new-recruitment'

def send_correction_email(name, email, pdf_path):
    try:
        msg = MIMEMultipart('mixed')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Bcc'] = BCC_EMAIL
        msg['Subject'] = "Re: Welcome Aboard – Blockchain Club, VIT Bhopal"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px; color: #111;">
            <p>Dear {name},</p>

            <p>
                Please note that the appointment letter shared earlier was sent incorrectly due to an oversight.
                Kindly find the <strong>correct appointment letter attached</strong> with this email and disregard the previous one.
            </p>

            <p>
                Best regards,<br>
                Blockchain Club VITB<br>
                VIT Bhopal University<br>
                blockchainclub@vitbhopal.ac.in
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(pdf_path)
                )
                msg.attach(attach)
        else:
            print(f"PDF not found for {name}")
            return False

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(
                EMAIL_ADDRESS,
                [email, BCC_EMAIL],
                msg.as_string()
            )

        print(f"[{datetime.now()}] CORRECTION SENT → {email}")
        return True

    except Exception as e:
        print(f"[{datetime.now()}] ERROR sending to {email}: {e}")
        return False

def process_csv_and_send_emails():
    df = pd.read_csv(INPUT_CSV_FILE)

    for _, row in df.iterrows():
        name = row['Name'].strip()
        email = row['emailID'].strip()

        pdf_name = f"Certificate_{name.replace(' ', '_')}.pdf"
        pdf_path = os.path.join(PDF_FOLDER, pdf_name)

        send_correction_email(name, email, pdf_path)
        time.sleep(2)

if __name__ == "__main__":
    process_csv_and_send_emails()
