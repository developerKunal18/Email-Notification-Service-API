from flask import Flask, request, jsonify
from email.message import EmailMessage
import smtplib
import threading

app = Flask(__name__)

# ---------- Email Sender ----------
def send_email(recipient, subject, body):

    try:
        email = EmailMessage()

        email["Subject"] = subject
        email["From"] = "your_email@gmail.com"
        email["To"] = recipient

        email.set_content(body)

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                "your_email@gmail.com",
                "your_app_password"
            )

            smtp.send_message(email)

    except Exception as e:
        print("Email Error:", e)

# ---------- API ----------
@app.route(
    "/send-email",
    methods=["POST"]
)
def send_notification():

    data = request.get_json()

    recipient = data["email"]
    subject = data["subject"]
    body = data["message"]

    thread = threading.Thread(
        target=send_email,
        args=(
            recipient,
            subject,
            body
        )
    )

    thread.start()

    return jsonify(
        {
            "message":
            "Email queued successfully"
        }
    )

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
