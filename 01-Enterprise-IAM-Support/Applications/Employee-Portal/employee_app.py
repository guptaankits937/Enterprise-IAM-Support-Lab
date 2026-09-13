from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["SESSION_COOKIE_NAME"] = "employee_portal_session"

KEYCLOAK_BASE = os.environ.get(
    "KEYCLOAK_BASE",
    "http://<KEYCLOAK_HOST>:8080"
)

REALM = "enterprise-iam-lab"
CLIENT_ID = "employee-portal"

METADATA_URL = (
    f"{KEYCLOAK_BASE}/realms/{REALM}/.well-known/openid-configuration"
)

oauth = OAuth(app)

oauth.register(
    name="keycloak",
    client_id=CLIENT_ID,
    server_metadata_url=METADATA_URL,
    client_kwargs={
        "scope": "openid profile email",
        "code_challenge_method": "S256",
        "token_endpoint_auth_method": "none",
    },
)


@app.route("/")
def home():
    user = session.get("user")

    if user:
        username = user.get("preferred_username", "unknown")

        return f"""
        <h1>Employee Portal</h1>
        <p>OIDC SSO Login Successful</p>
        <p>Logged in as: <strong>{username}</strong></p>
        <a href="/logout">Local Logout</a>
        """

    return """
    <h1>Employee Portal</h1>
    <p>You are not logged in.</p>
    <a href="/login">Login with Keycloak</a>
    """


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)


@app.route("/callback")
def callback():
    token = oauth.keycloak.authorize_access_token()

    user = token["userinfo"]
    session["user"] = dict(user)

    roles = user.get("realm_access", {}).get("roles", [])
    session["roles"] = roles

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
