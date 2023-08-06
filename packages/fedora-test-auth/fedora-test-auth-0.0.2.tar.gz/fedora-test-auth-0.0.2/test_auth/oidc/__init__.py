import json
from pprint import pformat

import flask
from authlib.integrations.flask_client import OAuth
from test_auth.utilities import create_flask_sub_app

# Set up Flask application
app = create_flask_sub_app(__name__)

# Set up OIDC extension
oauth = OAuth(app)

def load_client_secrets():
    with open(app.config.get("OIDC_CLIENT_SECRETS", "client_secrets.json")) as fh:
        config = json.load(fh)
    return config["web"]

oidc_config = load_client_secrets()

oauth.register(
    name='fedora',
    client_id=oidc_config["client_id"],
    client_secret=oidc_config["client_secret"],
    server_metadata_url=f"{oidc_config['issuer']}/.well-known/openid-configuration",
    # api_base_url=oidc_config["issuer"],
    client_kwargs={
        "scope": " ".join(app.config.get("OIDC_SCOPES", ["openid", "email"])),
        'token_endpoint_auth_method': app.config.get(
            "OIDC_INTROSPECTION_AUTH_METHOD",
            "client_secret_post"
        ),
    },
)

@app.before_request
def before_request():
    """Set the flask session as permanent."""
    flask.session.permanent = True


@app.route("/")
def home():
    if "oidc_profile" in flask.session:
        user_data = pformat(flask.session["oidc_profile"])
    else:
        user_data = None
    return flask.render_template("home.html", user_data=user_data)


@app.route("/login")
def login():
    redirect_uri = flask.url_for('authorize', _external=True)
    return oauth.fedora.authorize_redirect(redirect_uri)


@app.route('/oidc_callback')
def authorize():
    token = oauth.fedora.authorize_access_token()
    profile = oauth.fedora.userinfo(token=token)
    # Store those in the session for later access
    flask.session["oidc_token"] = token
    flask.session["oidc_profile"] = profile
    return flask.redirect(flask.url_for(".home"))


@app.route("/logout")
def logout():
    if "oidc_token" in flask.session:
        # Clear our data from the session
        del flask.session["oidc_token"]
        del flask.session["oidc_profile"]
        flask.flash("You have been logged out", "info")
    return flask.redirect(flask.url_for(".home"))
