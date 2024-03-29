import os
from subprocess import Popen

from flask import Flask, send_from_directory


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.sqlite3")

    from database import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
    # with app.app_context():
    #     db.create_all()

    from intrago.views import intrago
    from intrago.api import api

    app.register_blueprint(intrago, url_prefix="")
    app.register_blueprint(api, url_prefix="/api/v1")

    return app


if __name__ == "__main__":
    # Compile SCSS in real-time
    if os.environ["FLASK_DEBUG"] == "True":
        print("Starting SCSS compiler")
        scss = Popen(
            ["sass", "--watch", "assets/scss/main.scss:static/dist/bundle.css"]
        )
    app = create_app()

    # Favicon request
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static/icons"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    app.run(debug=True)
