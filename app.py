from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


app = Flask(__name__)

# Serve the frontend HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/send-emails', methods=['POST'])
def send_emails():
    try:
        subject = request.form['subject']
        file = request.files['spreadsheet']

        # Read the spreadsheet
        email_list = pd.read_excel(file)

        # SMTP setup
        FROM = "tayyabashraf629@gmail.com"  
        PASS = "qlar bvid eljt rfzz"
        SERVER = "smtp.gmail.com"
        PORT = 587

        server = smtplib.SMTP(SERVER, PORT)
        server.starttls()
        server.login(FROM, PASS)

        for _, row in email_list.iterrows():
            recipient_email = row['Email Address']
            recipient_name = row['Full name']

            msg = MIMEMultipart()
            msg['From'] = FROM
            msg['To'] = recipient_email
            msg['Subject'] = subject
            body = f"Hello {recipient_name},\n\nThis is a test email.\n\nRegards."
            msg.attach(MIMEText(body, 'plain'))

            server.sendmail(FROM, recipient_email, msg.as_string())

        server.quit()
        return jsonify({"message": "Emails sent successfully!"}), 200
    except Exception as e:
        return str(e), 500




if __name__ == '__main__':
    app.run(debug=True)
