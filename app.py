from email.mime.text import MIMEText
import smtplib

from flask import Flask, redirect, render_template, request, url_for
import os

app = Flask(__name__)

# 🔐 Use environment variables (VERY important)
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


@app.route("/")
def home():
    return render_template("xrwise_landingpage.html")

@app.route("/team")
def team():
    return render_template("xrwise_team.html")

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    user_email = data.get("email")

    if not user_email:
        return {"error": "Email required"}, 400

    try:
        msg = MIMEText(f"New demo request from: {user_email}")
        msg["Subject"] = "New XRwise Demo Request"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return {"success": True}, 200

    except Exception as e:
        print(e)
        return {"error": "Failed"}, 500

if __name__ == "__main__":
    # Only used for local development
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)