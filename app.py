from email.mime.text import MIMEText
from flask_mail import Message
import smtplib
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
import os
from config import Config
from extensions import mail

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)

@app.route("/")
def home():
    return render_template("xrwise_landingpage.html")

@app.route("/team")
def team():
    return render_template("xrwise_team.html")

# TODO Fix sending Email
@app.route("/send-email", methods=["POST"])
def send_email():

    try:
        data = request.get_json()
        user_email = data.get("email")

        if not user_email:
                return jsonify({"error": "Email required"}), 400

        send_request(user_email)

        return jsonify({"success": True}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route("/impressum")
def impressum():
    return render_template("impressum.html")


@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")

@app.route("/news")
def news():
    return render_template("news.html")

# Helper: Send Mail
def send_request(request_email):
    msg = Message("[XRWise] Demo-Anfrage", recipients=["luzie.ahrens@gmail.com"])
    msg.body = f'''Demo-Anfrage von: {request_email}'''

    try:
        mail.send(msg)
    except Exception as e:
        print("Nachricht konnte nicht erstellt werden", e)

if __name__ == "__main__":
    # Only used for local development
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)