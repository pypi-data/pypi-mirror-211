import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix

from .oidc import app as oidc_app
from .openid import app as openid_app
from .utilities import create_flask_app


root_app = create_flask_app(__name__)


@root_app.route("/")
def root():
    return flask.render_template("root.html")


application = DispatcherMiddleware(
    root_app, {"/oidc": oidc_app, "/openid": openid_app}
)

application = ProxyFix(application, x_proto=1, x_host=1)
