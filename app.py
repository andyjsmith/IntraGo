import os
from subprocess import Popen

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

    from database import db

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    db.init_app(app)

    from intrago.views import intrago
    from intrago.api import api

    app.register_blueprint(intrago, url_prefix="")
    app.register_blueprint(api, url_prefix="/api/v1")

    return app, db


def setup_database(app, db):
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    # Compile SCSS in real-time
    if os.environ["FLASK_ENV"] == "development":
        print("Starting SCSS compiler")
        scss = Popen(
            ["sass", "--watch", "assets/scss/main.scss", "static/dist/bundle.css"]
        )
    app, db = create_app()
    setup_database(app, db)

    app.run(debug=True)
