from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("xrwise_landingpage.html")

@app.route("/team")
def team():
    return render_template("xrwise_team.html")

if __name__ == "__main__":
    # Only used for local development
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)