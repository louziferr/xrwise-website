from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_babel import Babel, get_locale
from flask_mail import Message
from dotenv import load_dotenv
from extensions import mail
from config import Config
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.config['BABEL_DEFAULT_LOCALE'] = 'de'
app.config['BABEL_SUPPORTED_LOCALES'] = ['de', 'en']
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

mail.init_app(app)

def get_user_locale():
    # 1. Check session (set by language switcher)
    lang = session.get('lang')
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        return lang
    # 2. Fall back to browser preference
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

babel = Babel(app, locale_selector=get_user_locale)


# ── Language switcher route ──────────────────────────────────────────
@app.route("/set-lang/<lang>")
def set_lang(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

@app.context_processor
def inject_locale():
    return dict(get_locale=get_locale)

# ── Pages ────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("xrwise_landingpage.html")

@app.route("/team")
def team():
    return render_template("xrwise_team.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/impressum")
def impressum():
    return render_template("impressum.html")

@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")


# ── Email ────────────────────────────────────────────────────────────
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

def send_request(request_email):
    msg = Message("[XRWise] Demo-Anfrage", recipients=["luzie.ahrens@gmail.com"])
    msg.body = f"Demo-Anfrage von: {request_email}"
    try:
        mail.send(msg)
    except Exception as e:
        print("Nachricht konnte nicht erstellt werden", e)


if __name__ == "__main__":
    app.run(debug=True)