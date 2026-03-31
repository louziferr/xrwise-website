from email.mime.text import MIMEText
import smtplib
import resend
from flask import Flask, jsonify, redirect, render_template, request, url_for
import os

app = Flask(__name__)

# 🔐 Use environment variables (VERY important)
# Set API key
resend.api_key = os.environ.get("RESEND_API_KEY")

# Your email (where you receive requests)
TO_EMAIL = "la@xrwise.tech"


@app.route("/")
def home():
    return render_template("xrwise_landingpage.html")

@app.route("/team")
def team():
    return render_template("xrwise_team.html")

@app.route("/send-email", methods=["POST"])
def send_email():

    try:
        data = request.get_json()
        user_email = data.get("email")

        if not user_email:
                return jsonify({"error": "Email required"}), 400

        resend.Emails.send({
                "from": "onboarding@resend.dev",  # works out of the box
                "to": TO_EMAIL,
                "subject": "New XRwise Demo Request",
                "html": f"""
                    <h2>New Demo Request</h2>
                    <p><strong>Email:</strong> {user_email}</p>
                """
            })

        return jsonify({"success": True}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Only used for local development
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)