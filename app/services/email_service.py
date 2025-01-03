import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email, subject, body):
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_password = os.environ.get('GMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.close()
        print('Email sent!')
    except Exception as e:
        print(f'Something went wrong: {e}')

def mask_id(id_string):
    return '*' * (len(id_string) - 3) + id_string[-3:]

def send_personal_details_confirmation(email):
    subject = "Personal Details Submitted Successfully"
    body = "Your personal details have been submitted successfully. Please proceed with the next step of document upload and KYC verification."
    send_email(email, subject, body)

def send_document_upload_confirmation(email):
    subject = "Documents Uploaded Successfully"
    body = "All your documents have been successfully submitted. We will process your KYC verification shortly."
    send_email(email, subject, body)

def send_account_creation_confirmation(email, customer_id, account_id, password):
    masked_customer_id = mask_id(str(customer_id))
    masked_account_id = mask_id(str(account_id))
    subject = "Account Created Successfully"
    body = f"""
    Your account has been successfully created!
    
    Customer ID: {masked_customer_id}
    Account ID: {masked_account_id}
    Password: {password}

    Please keep this information safe and secure.
    """
    send_email(email, subject, body)

