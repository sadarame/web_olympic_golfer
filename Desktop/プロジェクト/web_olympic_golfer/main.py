import os
from flask import Flask, redirect, url_for, render_template, session, jsonify
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

google_bp = make_google_blueprint(
    scope=["profile", "email"],
    redirect_to="index"
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    user_info = None
    if google.authorized:
        try:
            resp = google.get("/oauth2/v2/userinfo")
            if resp.ok:
                user_info = resp.json()
                session['profile'] = user_info
        except Exception as e:
            print(f"Error fetching user info: {e}")
            # In case of token expiration or other issues, clear the session
            session.clear()

    return render_template("index.html", user_info=user_info)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)